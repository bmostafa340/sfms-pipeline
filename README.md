# sfms-pipeline
An efficient and automated pipeline for generating a selection of plots from raw photometry data.

# Overview:

At a high level, the goal of the pipeline is to facilitate reevaluation of galaxy properties with a more realistic model of the universe than that which is typically assumed. Specifically, it is conventionally assumed that all galaxies share a temperature of formation that is common with that of the Milky Way, whereas it is expected that the Milky Way's temperature of formation is very much on the low end. A potential consequence might have been that galaxy stellar masses and star formation rates have been overestimated. This pipeline attempts to fit a temperature-like parameter to each galaxy, and to incorporate this temperature in the estimation of galaxy properties in order to evaluate the consequences of the conventional assumption, as well as any temperature-related trends that might arise.

At a slightly lower level, the pipeline analyzes and visualizes large amounts of photometric data, with a focus on analyzing the so-called star-forming main sequence, a tight exponential relationship between galaxy stellar masses and star-formation rates that has been determined observationally but remains poorly understood. To do so efficiently, it breaks the overall process up into more manageable chunks, and uses a Makefile to automatically update dependencies only when necessary. Due to the hierarchical nature of the relevant processes, with many of the shared dependencies occupying far more time than the higher level processes, the design of the pipeline confers a great speed up on a typical process.

In general, the pipeline is organized as follows. The lowest level dependency is the classification of galaxies as star-forming or quiescent by means of UVJ color selection, which takes hours to days depending on the size of the data set and the computational power of the machine. Moving one step higher, each time EAZY is run to fit galaxies with a redshift and a best fit linear combinations of template spectra, 30 - 60 mins are required to translate the text output into npy format in order to speed up processing in future steps. One step higher from there, the computation of galaxy properties from the npy formatted output takes a few minutes. Most processes that depend on the computed galaxy properties run quickly. Generating plots that directly compare galaxy properties takes no more than a minute, and generating plots that analyze the direct comparisons to yield additional insight are similarly quick to run.

Many of the details about what the individual processes do have been abstracted away in the above discussion. More of these details are presented in the Usage section. Due to the specificity of the tools, data, and procedures involved, as well as the complicated nature of the dependencies, it will be quite hard to follow, and the user is not expected to be aware of all of these details.

# Usage:

Some necessary parameter and data files are omitted, since they are multiple GB in size. Some packages such as numpy, scipy, matplotlib, and EAZY would also have been required had this repository been intended for direct use.

In order to make the pipeline user friendly, a Makefile was written to automate the execution of a user-selected process, as well as its dependencies.

To use the Makefile, one must simply install make, and then issue the command "make 'target'" in order to build the desired target. Make targets are listed in the Makefile in the form "'target' :". Targets intended to be run directly by the user are commented in the Makefile.
  
To run the processes involved in the pipeline manually, one would need to follow the instructions below.

Prerequisites:

Update ROOT in Constants/constants.py to the path of sfms-pipeline.

If OUTPUT has changed, run generate_idtempz.py.

UVJ Selection:

If you already have a folder of param_files you want to use, replace Extra/Param_Files. The folder has to be named Param_Files and each param file has to be named param{temperature}. Otherwise, update Extra/param (template param file) and param_files.py (which copies param, replacing lines with temperature-dependent aspects) with your desired data, then run param_files.py.

Run eazy_uvj.py. This runs and stores EAZY’s UVJ flux calculations. This involves rerunning EAZY on all galaxies in idtempz.txt, but only for their correct temperature instead of all 53. But it is currently not parallized, so it takes a day or so to run.

Run glxy_uvj.py. This generates galaxy_uvj files from the output of eazy_uvj.py. galaxy_uvj files have three columns: ID, U-V, V-J.

Note: Will need to follow the instructions in Galaxy Properties as well to complete the classification.

Galaxy Properties:

If OUTPUT has changed, run update_constants.py (changes Constants/constants/NGAL to the # of galaxies in idtempz.txt) and aux_file_writer.py (records relevant zout file data in .npy format to increase read speed).

If 1K_Templates has changed, update nmf_reader.py/ROOT with the path to the new 1K_Templates. Run nmf_reader.py (stores relevant data in Extra/NMF_Props), then run bas_props.py (calculates basis template properties and stores in Computed_Files/Basis_Props).

Run glxy_props_pure_uvj.py (generates galaxy_properties_pure_uvj files, which contain all galaxy properties, including star-forming/quiescent galaxy classification assuming pure UVJ selection).

Run apply_sSFR_cut.py (generates galaxy_properties files, which are identical to the corresponding galaxy_properties_pure_uvj files, except applying an sSFR cut to the star-forming/quiescent galaxy selection). By default, star-forming galaxies are identified as in pure UVJ, but removing the bottom decile in sSFR. Similarly, quiescent galaxies are identified as in pure UVJ, but removing the upper decile in sSFR. To change this behavior, modify apply_sSFR_cut.py.

Plotting:

Note: galaxy_properties must be up to date in order for the generated plots to be correct.

To plot the SFMS colored by temperature, run plot_ms.py.

To plot the SFMS colored by density of points, run plot_hess.py (which also generates data about the best fit lines).

To plot best fit slopes vs age of the universe, ensure plot_hess.py has been run on the most recent data. Then run plot_slopes_z.py (which also calculates the best-fit slope as a linear function of time).

To plot best fit intercepts vs age of the universe, ensure plot_hess.py has been run on the most recent data. Then run plot_intercepts_z.py (which also calculates the best-fit intercept as a linear function of time).

To plot the UVJ diagram, run plot_uvj.py.

To plot T vs Z-red for quiescent galaxies, run plot_T_vs_z_quiescent.py.

To plot T vs Z-red for star-forming galaxies, run plot_T_vs_z_star-forming.py

Equations:

To print the best-fit slope vs age of universe equation, ensure Plotting/3 has been run with updated information. Then run z_slope_equation.py.

To print the best-fit intercept vs age of universe equation, ensure Plotting/4 has been run with updated information. Then run z_slope_equation.py.

To print the best-fit SFMS equation, ensure Plotting/3 and Plotting/4 have been run with updated information. Then run z_equation.py.

To print the LaTex code for the α-β table, ensure Plotting/3 and Plotting/4 have been run with updated information. Then run z_equation.py.
