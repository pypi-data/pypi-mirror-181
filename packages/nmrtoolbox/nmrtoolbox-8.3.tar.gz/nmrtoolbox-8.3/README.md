# nmrtoolbox

## Introduction
This is a simple utility that provides modules for working with NMRPipe peak tables and performing a receiver operator characteristic (ROC) analysis to quantify the quality of the "recovered" peaks relative to a control set of "injected" peaks.  The modules in this package are as follows:
- `nmrtoolbox.peak`: classes for reading in peak tables (currently supports both synthetically generated and recovered peak tables from NMRPipe)
- `nmrtoolbox.roc`: perform receiver operator characteristic (ROC) analysis of a recovered peak table relative to an injected peak table
- `nmrtoolbox.mask`: define regions of a spectrum that contain signal or are empty
- `nmrtoolbox.util`: various supporting utilities used by other modules

## Applications

### Example #1 - Formal Workflow
The tools in this package are utilized by the [NUScon](https://nuscon.org/home) software package.  You can access NUScon on the NMRbox platform (free for academic, government, and non-profit users).  Running `nuscon -h` will provide instructions on how to run the NUScon evaluation workflow, which directly utilizes the tools presented here in the `nmrtoolbox` package.

### Example #2 - Kick the Tires

```commandline
from nmrtoolbox.roc import roc

# perform ROC analysis and specify filtering criteria for 
# cluster_type and chi2prob
my_roc = roc(
    recovered_table=<file-recovered.tab>,
    injected_table=<file-injected.tab>,
    cluster_type=1,
    chi2prob=.75,
)

# show and plot results
my_roc.print_stats()
my_roc.plot_roc()
my_roc.plot_peaks()
my_roc.plot_outliers()
```

The roc function supports the following filter criteria:
- `number`
- `height` 
- `abs_height` 
- `roi_list` 
- `index`
- `cluster_type`
- `mask_file`
- `chi2prob`

Note: Filtering by `mask` requires the external use of NMRPipe to generate a mask file indicating where the spectrum is empty.  This binary data is converted by [Connjur Spectrum Translator](https://nmrbox.nmrhub.org/software/spectrum-translator) into a "tabular" format file (i.e. plain text) which is then read in by `nmrtoolbox.mask`.


## Changelog
v8
- change to MIT license
- box_radius for mask filtering is multidimensional
- improved input options for setting carrier frequency
- axis labels used to verify compatibility of Peak and Mask objects

v7
- addition of `roc` module
- addition of `mask` module

v6
- rename package as `nmrtoolbox`
- use subclasses to handle NMRPipe peak tables coming from genSimTab or from the peak picker

v5
- new Axis class for containing metadata from peak table header
