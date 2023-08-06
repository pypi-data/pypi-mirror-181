import numpy as np
from scipy.stats import chi2
from pathlib import Path
import re
from nmrtoolbox.util import Range, ROI, AxisData, TableData, PeakOutsideOfMaskError, ParsePeakTableError
from nmrtoolbox.mask import Mask


class Peak:
    """
    A container for the values that describe a peak.
    """
    def __init__(self, prop_list, val_list, axis_list):
        """
        Populate a peak

        :param prop_list: parameter names (from VARS line)
        :param val_list: parameter values (line from peak table)
        :param axis_list: names of axes (e.g. 'X', 'Y', 'Z')
        """
        if not (len(prop_list) == len(val_list)):
            raise ValueError('properties and values must be lists of the same length')

        self.axis_list = axis_list

        # use the character in the format string to convert each value accordingly
        self.prop = dict()
        for p, v in zip(prop_list, val_list):
            # try to convert the value to int or float; then accept it as string
            try:
                self.prop[p] = int(v)
                continue
            except ValueError:
                pass
            try:
                self.prop[p] = float(v)
                continue
            except ValueError:
                pass
            self.prop[p] = v

    def get_par(self, par, axis_list='all'):
        """
        Get value of specified parameter for specified axes.

        :param par: nmrPipe peak table parameter name (e.g. *_PPM, HEIGHT)
                    The * is substituted with axis values for each label requested
        :param axis_list: list of axis identifiers to include (e.g. 'X' or default of 'all')
        :return: singleton value or list of values
        """
        if '*' not in par:
            par_set = [par]
        else:
            par_set = []

            # determine which labels to query
            if axis_list == 'all':
                axis_list = self.axis_list
            if isinstance(axis_list, str):
                axis_list = [axis_list]

            # perform substitutions of axis names into parameter name as needed
            for axis in axis_list:
                if axis not in self.axis_list:
                    raise KeyError(f'invalid axis: {axis}')
                par_set.append(par.replace('*', axis))

        out = []
        for par in par_set:
            try:
                out.append(self.prop[par])
            except KeyError:
                raise KeyError(f'property not found: {par}')

        if len(out) == 1:
            return out[0]
        else:
            return out

    def get_par_list(self):
        return list(self.prop.keys())

    def set_par(self, par, value):
        """
        Change or create a new parameter

        :param par: parameter name
        :param value: corresponding value
        :return:
        """
        self.prop[par] = value

    def print(self):
        """Print all the key/value pairs that define the peak"""
        for k, v in self.prop.items():
            print(f"{k:8s}: {v:>15}")

    def in_roi(self, roi: ROI):
        """
        Check if current peak is within the given ROI

        :param roi: ROI class object
        :return: bool
        """
        if set(roi.axis_list()) != set(self.axis_list):
            raise ValueError('the current peak and the given ROI do not have same set of axes')

        return all([roi.range(axis).contains(self.get_par(f'{axis}_PPM')) for axis in self.axis_list])

    def in_mask(self, mask: Mask, box_radius=2):
        """
        determine if the peak position (and some neighborhood around it) is in empty region of mask
        """
        # TODO:
        #  the ordering of the dimensions in the Peak may not be consistent with ordering in Mask
        #  this info would be available from PeakTable.axis_property
        try:
            return mask.ppm_in_mask(
                peak_ppm=self.get_par('*_PPM'),
                box_radius=box_radius,
            )
        except PeakOutsideOfMaskError as e:
            print(e)
            return False


class PeakTable:
    """
    A class for containing a collection of peaks (e.g. from a peak picker or synthetic peak generator)
    Sub-classes are defined for each peak table file format.
    """
    def __init__(self, file, **kwargs):
        """
        Populate a peak list.  Each type of peak list file is sub-classed from PeakTable.  The subclasses should have
        an __init__ that defines "pre" operations, calls super.__init__, defines "post" operations.  The __init__ here
        includes pre operations for ALL PeakTable subclasses and it includes a call to _parse_file (which should be
        defined within each subclass).  The subclass __init__ should then call _post to run operations that are defined
        for ALL PeakTable subclasses.  By creating an instance of a subclass, the following operations are performed:
            "pre" operations in subclass __init__
            "pre" operations in PeakTable __init__
            _parse_file (defined by subclass)
            "post" operations in PeakTable __init__
            "post" operations in subclass __init__
            _post (defined by PeakTable)

        Here is a template for subclass definition

        class SomeNewSubclass(PeakTable):
            def __init__(self, file):
                # pre
                <define instance variables used specifically by this subclass>

                # call PeakTable.__init__ which includes:
                #   (1) "pre" operations for all subclasses
                #   (2) _parse_file method, which is defined by the subclass
                super().__init__(file, **kwargs)

                # post
                <perform operations after table file is parsed that are specific to this subclass>
                self._post() <- perform operations after the table file is parsed that are for ALL subclasses

        :param file: peak table file
        """
        self.file = Path(file)
        if not self.file.is_file():
            raise FileNotFoundError('peak table does not exist: {}'.format(self.file))

        # list of Peak objects
        self.peaks = []

        # metadata for each axis (e.g. X, Y, Z) - captured in an AxisData object:
        #   - labels (e.g.H1, N15)
        #   - num_pts
        #   - ppm_range (from ppm_high, ppm_low)
        self.axis_property = AxisData()

        # global properties that describe the collection of peaks
        self.table_property = TableData()

        # subclasses will each call _parse_file() to populate self.peaks and self.axis_property
        # subclasses can optionally include "pre" and "post" tasks in their __init__ to perform before/after parsing

        try:
            self._parse_file()
        except NotImplementedError as e:
            raise ParsePeakTableError(e)
        except ValueError as e:
            raise ParsePeakTableError(f'failed to read peak table: {self.file}\n{e}')
        except Exception as e:
            raise ParsePeakTableError(f'failed to read peak table: {self.file}\n{e}')

        try:
            self._set_carrier_frequency(**kwargs)
        except Exception as e:
            raise ParsePeakTableError(f'failed to set carrier frequency: {self.file}\n{e}')

    def _parse_file(self):
        """stub - subclasses must define this and populate self.peaks and self.axis"""
        raise NotImplementedError('sub-class must define a _parse_file() function')

    def _post(self):
        """operations to run after an instance of any subclass has been created"""
        try:
            self.get_par(par='*_HZ')
        except KeyError:
            try:
                self._set_peak_positions_hz()
            except KeyError:
                print('not able to compute peaks positions in Hz automatically')
                pass

    def _set_carrier_frequency(
            self, carrier_frequency=None, carrier_frequency_unit='MHz', **kwargs):
        # the injected peaks are presumed to be inserted into an empirical data set, so read the
        # carrier frequency out of the empirical peak table, because it is not included in the
        # injected peak table
        # carrier_frequency = self.empirical_table.axis_property.get(name='carrier_frequency')

        if carrier_frequency is None:
            # try to auto-determine carrier frequency from ppm and Hz values
            try:
                self._set_carrier_frequency_from_ppm_hz()
            except KeyError as e:
                raise KeyError(e)

        elif isinstance(carrier_frequency, AxisData):
            if set(carrier_frequency.axis_list()) != set(self.axis_property.axis_list()):
                raise AttributeError('The axes for the given carrier frequency data dot match those of the peak table')
            self.axis_property.set_data(carrier_frequency)

        else:
            # expect numerical data
            try:
                cf_values = np.asarray(carrier_frequency).astype(float, casting='safe')
            except (ValueError, TypeError):
                raise ValueError('unable to convert carrier frequency data')

            if cf_values.size != self.num_dims():
                raise AttributeError('number of carrier frequencies does not match number of peak table dimensions')

            if carrier_frequency_unit == 'Hz':
                cf_hz = cf_values
            elif carrier_frequency_unit == 'MHz':
                cf_hz = cf_values * 1e6
            else:
                raise ValueError(f'do not recognize unit for carrier frequency: {carrier_frequency_unit}')

            for ax, cf in zip(self.axis_list(), cf_hz):
                self.axis_property.set(
                    axis=ax,
                    name='carrier_frequency',
                    value=cf,
                    unit='Hz',
                )

    def _set_carrier_frequency_from_ppm_hz(self):
        """Determine carrier frequency from the ratio between peak positions in Hz and ppm"""
        # get average hz/ppm ratio across all peaks for each dimension
        # NOTE: peak tables from genSimTab do not have Hz values, so catch missing data
        try:
            ppm = self.get_par(par='*_PPM')
            hz = self.get_par(par='*_HZ')
            carrier = np.mean(hz / ppm, axis=0) * 1e6
        except KeyError as e:
            raise KeyError(e)

        for axis, cf in zip(self.axis_property.axis_list(), carrier):
            self.axis_property.set(
                axis=axis,
                name='carrier_frequency',
                value=cf,
                unit='Hz',
            )

    def _set_peak_positions_hz(self):
        """Use ppm peak positions and provided carrier frequencies to determine peak positions in Hz"""

        for axis in self.axis_list():
            try:
                peak_ppm = self.get_par(par=f'{axis}_PPM')
            except KeyError:
                raise KeyError(f'missing peak PPM data for axis: {axis}')
            try:
                unit = self.axis_property.get_field(name='carrier_frequency', axis=axis, field='unit')[0]
                value = self.axis_property.get_field(name='carrier_frequency', axis=axis, field='value')[0]
                if unit == 'Hz':
                    cf_mhz = value / 1e6
                elif unit == 'MHz':
                    cf_mhz = value
                else:
                    raise ValueError(f'do not recognize unit for carrier frequency: {unit}')
                peak_hz = peak_ppm * cf_mhz
            except KeyError:
                raise KeyError(f'missing carrier frequency for axis: {axis}')
            for idx, peak in enumerate(self.peaks):
                peak.set_par(par=f'{axis}_HZ', value=peak_hz[idx])

    def num_peaks(self):
        """
        Count the peaks in a peak list

        :return: count
        """
        return len(self.peaks)

    def get_peak(self, index):
        """
        Get a peak, specified by index

        :param index: index within PeakTable (not necessarily same as "index" in the tab file)
        :return: PipePeak
        """
        try:
            return self.peaks[index]
        except IndexError:
            raise IndexError('asking for index = {:d}, max index = {:d}'.format(index, len(self.peaks)))

    def get_par(self, par, axis_list='all'):
        """
        Get all values for specified parameter for all peaks for specified axes.

        :param par: nmrPipe peak table parameter name (e.g. *_PPM, HEIGHT)
                    The * is substituted with axis values for each label requested
        :param axis_list: list of axis identifiers to include (e.g. 'X' or default of 'all')
        :return: numpy array
        """
        out = []
        for peak in self.peaks:
            out.append(peak.get_par(
                par=par,
                axis_list=axis_list,
            ))
        return np.array(out)

    def get_par_list(self):
        return self.peaks[0].get_par_list()

    def reduce(
            self,
            number=None,
            height=None,
            abs_height=None,
            roi=None,
            index=None,
            cluster_type=None,
            mask=None,
            box_radius=2,
            chi2prob=None,
    ):
        """
        reduce the peak list using filter criteria

        :param number: number of peaks to keep according to absolute value of peak HEIGHT
        :param height: keep all peaks with at least this HEIGHT
        :param abs_height: keep all peaks with absolute value at least this HEIGHT
        :param roi: keep peaks within the given ROI
        :param index: keep only peaks with given index values
        :param cluster_type: keep only peaks with given cluster type index
            NMRPipe currently uses: 1 = Peak, 2 = Random Noise, 3 = Truncation artifact
        :param mask: mask of True/False values on indel grid (e.g. use empirical peak table to set empty region)
        :param box_radius: defines size of box around peak position when querying it against empty mask
        :param chi2prob: remove peaks whose widths are outliers along any of the dimensions using chi2 probability
            expressed as p-value on [0,1] interval
        :return:
        """
        if number is not None:
            self.order_by_height()
            try:
                self.peaks = self.peaks[:number]
            except IndexError:
                # if the number of requested peaks is larger than number of actual peaks, just ignore and keep all
                pass

        elif height is not None:
            self.peaks = [p for p in self.peaks if p.get_par('HEIGHT') >= height]

        elif abs_height is not None:
            self.peaks = [p for p in self.peaks if abs(p.get_par('HEIGHT')) >= abs_height]

        elif roi is not None:
            if not isinstance(roi, ROI):
                raise TypeError('when reducing PeakTable by ROI, you must provide ROI class object')
            self.peaks = [p for p in self.peaks if p.in_roi(roi)]

        elif index is not None:
            if not isinstance(index, (list, tuple)):
                index = [index]
            try:
                self.peaks = [self.peaks[idx] for idx in index]
            except IndexError:
                raise IndexError('invalid index values for peak list')

        elif cluster_type is not None:
            if cluster_type not in [1, 2, 3]:
                print('NMRPipe peaks are categorized as:')
                print('  1 = Peak, 2 = Random Noise, 3 = Truncation artifact')
                raise TypeError('NMRPipe cluster_type must be one of the values above')
            self.peaks = [p for p in self.peaks if p.get_par('TYPE') == cluster_type]

        elif mask is not None:
            if not isinstance(mask, Mask):
                raise ValueError(f'provided mask should be of type nmrtoolbox.Mask (you provided {type(mask)}')
            self.peaks = [p for p in self.peaks if p.in_mask(mask=mask, box_radius=box_radius)]

        elif chi2prob is not None:
            idx_keep, idx_outlier = self.determine_outliers(chi2prob)
            self.reduce(index=idx_keep)

    def order_by_height(self):
        """Reorder the peak list by HEIGHT (positive down to negative)"""
        self.peaks = sorted(self.peaks, key=lambda x: x.prop['HEIGHT'], reverse=True)

    def axis_list(self):
        """Get the axis names"""
        return list(self.axis_property.axis_list())

    def num_dims(self):
        """Number of dimensions"""
        return len(self.axis_list())

    def label_list(self):
        """Get the axis labels"""
        return self.axis_property.get_field(name='label')

    def axis_label_list(self):
        """Get a list of tuples where each contains an axis and its label"""
        return [(ax, lab) for ax, lab in zip(self.axis_list(), self.label_list())]

    def determine_outliers(self, chi2prob):
        # get full width of each recovered peak in points along each of its dimensions
        w = self.get_par('*W')

        # Covariance matrix
        covariance = np.cov(w, rowvar=False)

        # Covariance matrix power of -1
        covariance_pm1 = np.linalg.matrix_power(covariance, -1)

        # Center point
        centerpoint = np.mean(w, axis=0)

        # the width of each peak along each dimension is compared to the mean width of all peaks along the dimension
        # the covariance matrix is used to normalize
        distances = (np.matmul(w - centerpoint, covariance_pm1) * (w - centerpoint)).sum(axis=1)

        # Cutoff (threshold) value from Chi-Square Distribution for detecting outliers
        cutoff = chi2.ppf(chi2prob, w.shape[1])

        # TODO
        #  stupid [0] needed to get ndarray out of tuple
        #  for now: put ndarray into list because PeakTable.reduce() seems to fail when index is provided as ndarray
        idx_keep = [x for x in np.where(distances <= cutoff)[0]]
        idx_outlier = [x for x in np.where(distances > cutoff)[0]]

        # return these lists so that other downstream analysis can be performed
        return idx_keep, idx_outlier


class PeakTablePipe(PeakTable):
    def __init__(self, file, **kwargs):
        """
        This class has subclasses for peak tables coming from INJECTED and RECOVERED peak tables; use those subclasses.
        You probably don't want to create a PeakTablePipe object - it is just a super-class to provide common tasks.
        """
        # pre
        self.VARS = None
        self.FORMAT = None

        super().__init__(file, **kwargs)

    def _parse_file(self):
        """
        Parser for peak tables from NMRPipe generated by peak picker (i.e. "REC") OR by genSimTab (i.e. "INJ").
        The PeakTablePipe class is subclassed to handle the differences in data presented in RECOVERED and INJECTED.
        """

        with open(self.file, 'r') as f_in:
            mode = None
            for line in f_in:
                line = line.strip()
                if line in ['', '#']:
                    continue

                if mode is None:
                    # recovered peak table starts with REMARK section
                    # injected peak table starts with genSimTab
                    if line.startswith('REMARK'):
                        mode = 'remark'
                    elif re.match('# [a-zA-Z_]*genSimTab.tcl', line):
                        # several variants of genSimTab.tcl are in use, so find all lines that might look like:
                        #   # genSimTab.tcl
                        #   # xzy_genSimTab.tcl
                        #   # new_genSimTab.tcl
                        mode = 'genSimTab'
                    else:
                        continue

                if mode == 'remark':
                    if line.startswith('REMARK'):
                        self.REMARK.append(line)
                        continue
                    else:
                        mode = 'data'

                if mode == 'genSimTab':
                    if line.startswith('#'):
                        self.genSimTab.append(line.strip().lstrip('#').rstrip('\\').strip())
                        continue
                    else:
                        mode = 'data'

                if mode == 'data':
                    if line.startswith('DATA'):
                        # axis properties are described like this
                        # example: DATA  X_AXIS HN           1   659   10.297ppm    5.798ppm
                        info = line.split()
                        try:
                            if info[1] == 'CLUSTER':
                                # some filtered peak tables include CLUSTER info - ignore these lines
                                # example: DATA  CLUSTER X_AXIS +/- 7
                                continue
                            elif info[1].endswith('_AXIS'):
                                axis = info[1].split('_')[0]
                                self.axis_property.set(
                                    axis=axis,
                                    name='label',
                                    value=info[2],
                                )
                                self.axis_property.set(
                                    axis=axis,
                                    name='num_pts',
                                    value=int(info[4]),
                                    unit='count'
                                )
                                self.axis_property.set(
                                    axis=axis,
                                    name='range',
                                    value=Range(
                                            min=float(info[5].rstrip('pm')),
                                            max=float(info[6].rstrip('pm')),
                                        ),
                                    unit='ppm',
                                )
                                continue
                            else:
                                raise ValueError(f'unrecognized line in peak table: {line}')
                        except (IndexError, ValueError):
                            raise ValueError('metadata missing from peak table header')
                    else:
                        mode = 'vars'

                if mode == 'vars':
                    if line.startswith('VARS'):
                        self.VARS = line.split()[1:]
                        # this is a single line of data, so get it and move on to next mode
                        mode = 'format'
                        continue

                if mode == 'format':
                    if line.startswith('FORMAT'):
                        self.FORMAT = line.split()[1:]
                        # this is a single line of data, so get it and move on to next mode
                        mode = 'peak'
                        continue

                if mode == 'peak':
                    if line.startswith('#'):
                        # comments are mixed into the synthetic peak lists - just ignore them
                        continue
                    else:
                        self.peaks.append(Peak(
                            prop_list=self.VARS,
                            val_list=line.split(),
                            axis_list=self.axis_list(),
                        ))


class PeakTablePipeRec(PeakTablePipe):
    """This subclass is for capturing the peaks "recovered" from an experiment by the NMRPipe peak picker"""
    def __init__(self, file, **kwargs):
        # pre
        self.REMARK = []

        try:
            super().__init__(file, **kwargs)
        except:
            raise ParsePeakTableError(f'failed to read peak table as type: PeakTablePipeRec\n{file}')

        # post
        self._get_noise()
        self._get_category_count()
        self._get_LW()

        self._post()

    def _get_LW(self):
        try:
            LW_list = self.get_par('*W').mean(axis=0)
        except KeyError as e:
            raise KeyError(e)

        for axis, LW in zip(self.axis_property.axis_list(), LW_list):
            self.axis_property.set(
                axis=axis,
                name='LW',
                value=LW,
                unit='pts',
            )

    def _get_noise(self):
        for line in self.REMARK:
            if line.startswith('REMARK Noise:'):
                # example: "REMARK Noise: 91905.9, Chi2-Threshold: 1.000000e-04, Local Adjustment: None"
                self.table_property.set(
                    name='noise',
                    value=float(line.split()[2].strip(',')),
                    unit='au',
                )

    def _get_category_count(self):
        for line in self.REMARK:
            if line.startswith('REMARK Total Peaks:'):
                # example: "REMARK Total Peaks: 60425, Good Peaks: 40513, Questionable Peaks: 19912"
                self.table_property.set(
                    name='peak_count_total',
                    value=int(line.split()[3].strip(',')),
                    unit='count'
                )
                self.table_property.set(
                    name='peak_count_good',
                    value=int(line.split()[6].strip(',')),
                    unit='count',
                )
                self.table_property.set(
                    name='peak_count_questionable',
                    value=int(line.split()[9].strip(',')),
                    unit='count',
                )


class PeakTablePipeInj(PeakTablePipe):
    """This subclass is for capturing the synthetic peaks "injected" by the NMRPipe genSimTab.tcl tool"""
    def __init__(self, file, **kwargs):
        """
        :param carrier_frequency: either a list of values in MHz or an AxisData object (e.g. from another PeakTable)
        """
        # pre
        self.genSimTab = []

        try:
            super().__init__(file, **kwargs)
        except:
            raise ParsePeakTableError(f'failed to read peak table as type: PeakTablePipeInj\n{file}')

        # post
        self.genSimTab = ' '.join(self.genSimTab)
        self._set_maxLW()
        self._post()

    def _set_maxLW(self):
        # parse through the tokens to find maxLW values for each axis
        tokens = self.genSimTab.split()
        for axis in self.axis_list():
            try:
                idx = tokens.index(f'-{axis.lower()}wMax')
                self.axis_property.set(
                    axis=axis,
                    name='maxLW',
                    value=float(tokens[idx + 1]),
                    unit='Hz',
                )
            except (ValueError, IndexError):
                pass
