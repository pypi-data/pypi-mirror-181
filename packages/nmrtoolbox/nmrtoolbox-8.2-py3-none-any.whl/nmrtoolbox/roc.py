#!/usr/bin/env python3
import time

import copy
import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.spatial import distance_matrix
from itertools import combinations

from nmrtoolbox.peak import PeakTable, PeakTablePipeRec, PeakTablePipeInj
from nmrtoolbox.util import ROI, ParsePeakTableError, pairwise_weighted_norm
from nmrtoolbox.mask import Mask


class roc:
    """
    A class for performing receiver operator characteristic (ROC) analysis on NMR peak lists
    """

    def __init__(
            self,
            recovered_table,
            injected_table,
            lw_scalar=1,
            number=None,
            height=None,
            abs_height=None,
            roi_list: list = None,
            index=None,
            cluster_type=None,
            mask_file=None,
            box_radius=2,
            chi2prob=None,
    ):
        """
        :param recovered_table: table (file) of recovered peaks from NMRPipe->pkDetect3D.tcl
        :param injected_table: table (file) of synthetic peaks from NMRPipe->genSimTab.tcl
        :param lw_scalar: scalar of an injected peak's linewidth to define a region in which a recovered peak is valid
        :param number: number of peaks to keep according to absolute value of peak HEIGHT
        :param height: keep all peaks with at least this HEIGHT
        :param abs_height: keep all peaks with absolute value at least this HEIGHT
        :param roi_list: region of interest to filter the recovered_peaklist
            by in order to assess for corresponding synthetic peaks,
            format is a list of [x_lower_bound_ppm, x_upper_bound_ppm, y_lower_bound_ppm, y_upper_bound_ppm, ...]
        :param index: keep only peaks with given index values
        :param cluster_type: keep only peaks with given cluster type index
            NMRPipe currently uses: 1 = Peak, 2 = Random Noise, 3 = Truncation artifact
        :param mask_file: spectra of the empty region used to filter out empirical from synthetic injected spectra that
            ROC is looking to recover; an alternative to providing an already filtered peaklist
        :param box_radius: defines size of box around peak position when querying it against empty mask
        :param chi2prob: remove peaks whose widths are outliers along any of the dimensions using chi2 probability
            expressed as p-value on [0,1] interval
        """
        # This ROC class accepts filtering criteria as a convenience to users so they do not have to read in peak tables
        # and call filtering functions before running roc.  So process the inputs for the peak table files and the roi
        # and then call the peak.reduce command to handle the rest.

        # ================================================
        if isinstance(recovered_table, PeakTable):
            self.recovered_peaks = recovered_table
        else:
            try:
                self.recovered_peaks = PeakTablePipeRec(
                    file=recovered_table,
                )
            except FileNotFoundError as e:
                raise FileNotFoundError(e)
            except ParsePeakTableError as e:
                raise ParsePeakTableError(e)

        # ================================================
        if isinstance(injected_table, PeakTable):
            self.injected_peaks = injected_table
        else:
            try:
                self.injected_peaks = PeakTablePipeInj(
                    file=injected_table,
                    carrier_frequency=self.recovered_peaks.axis_property.get('carrier_frequency'))
            except FileNotFoundError as e:
                raise FileNotFoundError(e)
            except ParsePeakTableError as e:
                raise ParsePeakTableError(e)

        # ================================================
        # validate some aspects of the peak table metadata and then move on to filtering operations
        self._validate_input()

        # ================================================
        self.roi = None
        if roi_list is not None:
            axis_list = self.injected_peaks.axis_list()
            if len(roi_list) != 2*len(axis_list):
                raise ValueError('there should be a min and max value in ppm for each axis')

            range_list = []
            while roi_list:
                range_list.append([roi_list.pop(0), roi_list.pop(0)])

            self.roi = ROI(
                axis_list=axis_list,
                range_list=range_list,
            )

        # ================================================
        self.mask = None
        if mask_file is not None:
            print('Reading mask file.  This may take a while...')

            self.mask_file = mask_file
            self.mask = Mask(file=self.mask_file)

        # ================================================
        # Get the max LW values used by genSimTab and then expand by a lw_scalar to define the distance along each axis
        # used to define if a recovered peak is within the accepted range of an injected peak to be considered a match.
        self.lw_scalar = lw_scalar
        self.peak_range_hz = np.array(self.injected_peaks.axis_property.get_field('maxLW')) * self.lw_scalar

        # ================================================
        # run the reduce commands (if any parameters are not given to roc, then they are None and reduce skips them)
        self.recovered_peaks.reduce(number=number)
        self.recovered_peaks.reduce(height=height)
        self.recovered_peaks.reduce(abs_height=abs_height)
        self.recovered_peaks.reduce(roi=self.roi)
        self.recovered_peaks.reduce(index=index)
        self.recovered_peaks.reduce(cluster_type=cluster_type)
        self.recovered_peaks.reduce(
            mask=self.mask,
            box_radius=box_radius,
        )

        # ================================================
        if chi2prob is not None:
            # could do this directly with: self.recovered_peaks.reduce(chi2prob=chi2prob)
            # BUT: the commands of reduce are reproduced here so that intermediate data can be captured
            # and used for outlier plotting

            # save instances of ALL peaks before removing the outlier peaks
            self.recovered_peaks_all = copy.deepcopy(self.recovered_peaks)
            self.recovered_peaks_outliers = copy.deepcopy(self.recovered_peaks)

            # partition all peaks into outliers and not outliers
            idx_keep, idx_outlier = self.recovered_peaks.determine_outliers(chi2prob=chi2prob)
            self.recovered_peaks_outliers.reduce(index=idx_outlier)
            self.recovered_peaks.reduce(index=idx_keep)

        # ================================================
        # create instance variables to capture the output from running ROC and then run ROC
        # initialize the RR and FDR lists to include the origin
        self.RR = [0]
        self.FDR = [0]
        self.recovered_peaks_true_ppm = []
        self.recovered_peaks_false_ppm = []
        self._recovery_rate()

        # compute metrics from ROC data
        self.AUC = self._AUC()
        self.DPC, self.DPC_index = self._DPC()
        self.MRMF = self._MRMF()

    def _validate_input(self):
        # sometimes proton is labeled as 1H or HN, so standardize on the more common HN
        if '1H' in self.recovered_peaks.label_list() and 'HN' in self.injected_peaks.label_list():
            for axis, label in self.recovered_peaks.axis_label_list():
                if label == '1H':
                    self.recovered_peaks.axis[axis].label = 'HN'

        if set(self.injected_peaks.label_list()) != set(self.recovered_peaks.label_list()):
            raise ValueError('The injected and recovered peak tables have different axis labels.')

        if hasattr(self, 'roi'):
            if len(self.injected_peaks.axis_list()) != len(self.roi.axis_list()):
                raise ValueError(
                    'Number of dimensions for injected and recovered peak lists are not in agreement with ROI list')

        if self.injected_peaks.num_peaks() == 0:
            raise ValueError('No recorded peaks in injected peak table')

        if self.recovered_peaks.num_peaks() == 0:
            raise ValueError('No peaks recovered by peak picker')

    def _recovery_rate(self):
        # ordering of peaks matters
        # sort the recovered peaks by height
        #   => the most intense recovered peaks have priority in being matched to closest injected peaks
        self.recovered_peaks.order_by_height()

        injected_peaks_hz = self.injected_peaks.get_par(par="*_HZ")
        recovered_peaks_hz = self.recovered_peaks.get_par(par="*_HZ")
        recovered_peaks_ppm = self.recovered_peaks.get_par(par="*_PPM")

        # compute pairwise distances between recovered and injected peaks - to be used for defining matches
        #  Currently finding closest injected peak to each recovered peak with unweighted L2, but at least it is in
        #  Hz and not ppm.  Eventually, the closest match identified here is more accurately assessed below by taking
        #  the distance along each axis and comparing to a cutoff distance defined as multiple of linewidth.
        #  Q: Is it possible that unweighted L2 matches incorrect injected peak to a recovered peak?
        #  A: Maybe.  But...
        #       - it's probably a recovered peak that isn't even near an injected peak
        #       - running several recovered peak tables through this shows that both methods yield same result
        #       - compute times are roughly 100:1 ratio (weighted vs unweighted) but on the order of 5s vs .05s
        #  Conclusion: just use unweighted L2 for now - can always toggle over to weighted L2, but must define weights
        pairwise_dist = distance_matrix(recovered_peaks_hz, injected_peaks_hz)
        # pairwise_dist = pairwise_weighted_norm(
        #     A=recovered_peaks_hz,
        #     B=injected_peaks_hz,
        #     w=np.array([1] * self.recovered_peaks.num_dims()),
        # )

        # for each recovered peak find the closest injected peak
        idx_recovered2injected = np.argmin(pairwise_dist, axis=1)

        # running tallies used to compute the recovery rate and false discovery rate
        count_true = 0
        count_false = 0

        # start with all injected peaks and remove them as they are matched to a recovered peak
        idx_injected_peak_available = set(range(self.injected_peaks.num_peaks()))

        for idx_recovered_peak, idx_injected_peak in enumerate(idx_recovered2injected):
            # distance along each axis from injected to nearest recovered peak
            distance_hz = np.abs(recovered_peaks_hz[idx_recovered_peak] - injected_peaks_hz[idx_injected_peak])

            # check if the closest injected peak is still available AND if it's inside the allowable neighborhood
            if (idx_injected_peak in idx_injected_peak_available) and (distance_hz <= self.peak_range_hz).all():
                count_true += 1
                self.recovered_peaks_true_ppm.append(recovered_peaks_ppm[idx_recovered_peak])
                idx_injected_peak_available.remove(idx_injected_peak)
            else:
                count_false += 1
                self.recovered_peaks_false_ppm.append(recovered_peaks_ppm[idx_recovered_peak])

            self.FDR.append(count_false / (count_false+count_true))
            self.RR.append(count_true / self.injected_peaks.num_peaks())

        # Appending the top right corner (extending the "plateau" of the ROC curve to reach the right edge)
        self.FDR.append(1)
        self.RR.append(max(self.RR))

        # Appending the bottom right corner
        self.FDR.append(1)
        self.RR.append(0)

    def _DPC(self):
        corner = np.array([[0, 1]])
        roc = np.column_stack((self.FDR, self.RR))
        dst = distance_matrix(corner, roc)

        dpc = np.min(dst)
        dpc_index = np.argmin(dst)

        return dpc, dpc_index

    def _AUC(self):
        """Area under the curve"""
        if len(self.RR) == len(self.FDR):
            n = len(self.RR)  # number of corners
        else:
            raise ValueError('RR and FDR are not the same length')

        # reference: https://math.stackexchange.com/questions/492407/area-of-an-irregular-polygon
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += self.FDR[i] * self.RR[j]
            area -= self.FDR[j] * self.RR[i]
        area = abs(area) / 2.0

        return area

    def _MRMF(self):
        """Maximum Recovery at Minimum False"""
        # construct an iterator that finds the first false positive and returns the previous index
        # use next() to only evaluate the iterator until the first result is found
        # provide len(self.FDR) as default in case no false positive is found
        idx = next((i-1 for i, v in enumerate(self.FDR) if v > 0), len(self.FDR))

        # if the very first recovered peak is false, that would result in an invalid idx=-1 (catch that case)
        # otherwise return the recovery rate at the index
        if idx >= 0:
            return self.RR[idx]
        else:
            return 0

    def print_stats(self):
        print(f"AUC: {self.AUC:5.4f}")
        print(f"DPC: {self.DPC:5.4f}")
        print(f"DPC_index: {self.DPC_index:d}")
        print(f"MRMF: {self.MRMF:5.4f}")

    def plot_outliers(self, file_out='outliers.pdf', show_figure=False):
        """Plot histograms of peak widths for all recovered peaks and for outliers vs keepers"""

        try:
            peak_width_all = self.recovered_peaks_all.get_par(par="*W")
            peak_width_keep = self.recovered_peaks.get_par(par="*W")
            peak_width_out = self.recovered_peaks_outliers.get_par(par="*W")
        except AttributeError:
            print('can only plot outlier data if you use chi2prob outlier filtering')
            return

        fig, axs = plt.subplots(3, 3, sharex='col', sharey='col')
        plt.suptitle('Histograms of recovered peak widths')
        # iterate through dimension indices (columns of the figure)
        for dim in [0, 1, 2]:
            # row 0: peak widths for ALL peaks on dimension
            ax = axs[0, dim]
            n, bins, patches = ax.hist([p[dim] for p in peak_width_all], bins=20)
            ax.set_xlim(.9*np.min(bins), 1.1*np.max(bins))
            ax.set_ylim(-0.1*np.max(n), 1.1*np.max(n))
            ax.set_title(self.recovered_peaks.label_list()[dim])

            # row 1: peak widths for KEEPERS on dimension
            ax = axs[1, dim]
            ax.hist([p[dim] for p in peak_width_keep], bins=bins)

            # row 2: peak widths for OUTLIERS on dimension
            ax = axs[2, dim]
            ax.hist([p[dim] for p in peak_width_out], bins=bins)

        for a in axs[-1, :]:
            a.set_xlabel('peak width\n[points]')
        axs[0, 0].set_ylabel('ALL\n[count]')
        axs[1, 0].set_ylabel('KEEPER\n[count]')
        axs[2, 0].set_ylabel('OUTLIER\n[count]')
        fig.tight_layout()

        Path(file_out).parent.absolute().mkdir(exist_ok=True)
        fig.savefig(file_out, format='pdf', dpi=1200)
        if show_figure:
            plt.show()
        plt.close()

    def plot_roc(self, file_out='ROC.pdf', show_figure=False):

        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        plt.xlabel('False Discovery Rate', fontsize=14)
        plt.ylabel('Recovery Rate', fontsize=14)
        plt.plot(self.FDR[:-1], self.RR[:-1],
                 marker='o', mew=0, mfc='blue', ms=6,   # marker properties
                 c='.7', lw=2,                          # line properties
                 label='ROC curve',
                 zorder=1)
        plt.xlim(-0.02, 1.02)
        plt.ylim(-0.02, 1.02)

        # put a big red dot on the point that is closest to perfect classifier
        plt.scatter(self.FDR[self.DPC_index], self.RR[self.DPC_index],
                    marker='s', c='red', s=30,
                    label='DPC reference',
                    zorder=2)

        plt.legend(loc='lower right')

        Path(file_out).parent.absolute().mkdir(exist_ok=True)
        fig.savefig(file_out, format='pdf', dpi=1200)
        if show_figure:
            plt.show()
        plt.close()

    def plot_peaks(self, dir_out=os.getcwd(), file_basename='peaks', show_figure=False):

        # TODO: this axis and dimension handling is very confusing
        num_dim = len(self.injected_peaks.axis_list())
        temp_slice_axes = combinations(list(range(1, num_dim + 1)), 2)
        slice_axes = [i for i in temp_slice_axes]

        injected_peaks_ppm = self.injected_peaks.get_par(par="*_PPM")

        for dims in slice_axes:
            xdim = int(dims[0]) - 1
            ydim = int(dims[1]) - 1

            inj_xdim_ppm = [p[xdim] for p in injected_peaks_ppm]
            inj_ydim_ppm = [p[ydim] for p in injected_peaks_ppm]

            trueRecov_xdim_ppm = [p[xdim] for p in self.recovered_peaks_true_ppm]
            trueRecov_ydim_ppm = [p[ydim] for p in self.recovered_peaks_true_ppm]

            falseRecov_xdim_ppm = [p[xdim] for p in self.recovered_peaks_false_ppm]
            falseRecov_ydim_ppm = [p[ydim] for p in self.recovered_peaks_false_ppm]

            fig, ax = plt.subplots()
            fig.subplots_adjust(right=0.75)
            plt.xlabel(f"{self.recovered_peaks.label_list()[xdim]} Domain [ppm]")
            plt.ylabel(f"{self.recovered_peaks.label_list()[ydim]} Domain [ppm]")
            plt.scatter(trueRecov_xdim_ppm, trueRecov_ydim_ppm,
                        c='#C5C9C7', marker='s', label='True Recovered')
            plt.scatter(falseRecov_xdim_ppm, falseRecov_ydim_ppm,
                        c='k', marker='x', label='Falsely Recovered')
            plt.scatter(inj_xdim_ppm, inj_ydim_ppm,
                        c='g', marker='v', label='injected')
            plt.legend(loc=(1.02, 0.15), prop={'size': 8})
            plt.title("Categorization of recovered peaks relative to injected peaks",
                         fontsize=10)

            filename = f"{file_basename}_{xdim + 1}_{ydim + 1}.pdf"
            file_out = Path(dir_out) / filename
            Path(file_out).parent.absolute().mkdir(exist_ok=True)

            plt.savefig(file_out, format='pdf', dpi=1200)
            if show_figure:
                plt.show()
            plt.close()


def parse_args():
    parser = argparse.ArgumentParser(description='You can add a description here')
    parser.add_argument('--recovered_table', required=True)
    parser.add_argument('--injected_table', required=True)
    parser.add_argument('--lw_scalar', type=float,
                        help='scalar multiple of linewidth for injected peak to define valid region for recovered peak')
    parser.add_argument('--number', type=int,
                        help='number of peaks to keep (starting from most intense)')
    parser.add_argument('--height', type=float,
                        help='')
    parser.add_argument('--abs_height', type=float,
                        help='')
    parser.add_argument('--roi_list', nargs='*', type=float,
                        help='min and max values in ppm for each dimension (min1 max1 min2 max2 ...)')
    parser.add_argument('--index', nargs='*', type=int,
                        help='peak indices to keep (indexing by position in peak list, NOT by indexing embedded in peak file)')
    parser.add_argument('--cluster_type', choices=[1, 2, 3],
                        help='keep only peaks with given cluster type index. NMRPipe currently uses: 1 = Peak, 2 = Random Noise, 3 = Truncation artifact')
    parser.add_argument('--mask_file', type=str,
                        help='path to file containing the mask of the empty region (tabular format from ConnjurST')
    parser.add_argument('--box_radius', type=int,
                        help='size of box around peak position when querying it against empty mask')
    parser.add_argument('--chi2prob', type=float,
                        help='chi square probability [0-1] used to remove peaks with outlier width')
    parser.add_argument('--print_stats', action='store_true',
                        help='print all ROC metric values to stdout')
    parser.add_argument('--plot_roc', action='store_true',
                        help='generate the roc plot and save to file')
    parser.add_argument('--plot_outliers', action='store_true',
                        help='generate histogram of outlier peaks if chi2prob is used for outlier removal')
    parser.add_argument('--plot_peaks', action='store_true',
                        help='generate projections of injected and recovered peak positions and save to file')
    return parser.parse_args()


def main():
    # parse the arguments from command line input and execute the nuscon workflow
    args = parse_args()

    try:
        my_roc = roc(
            recovered_table=args.recovered_table,
            injected_table=args.injected_table,
            lw_scalar=args.lw_scalar,
            number=args.number,
            height=args.height,
            abs_height=args.abs_height,
            roi_list=args.roi_list,
            index=args.index,
            cluster_type=args.cluster_type,
            mask_file=args.mask_file,
            box_radius=args.box_radius,
            chi2prob=args.chi2prob,
        )
        if args.print_stats:
            my_roc.print_stats()
        if args.plot_roc:
            my_roc.plot_roc()
        if args.plot_outlier:
            my_roc.plot_outliers()
        if args.plot_peaks:
            my_roc.plot_peaks()

    except (SystemExit, EnvironmentError, OSError) as e:
        print(e)
        sys.exit()
