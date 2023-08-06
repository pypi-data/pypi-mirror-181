====================
PDFstream Change Log
====================

.. current developments

v0.6.2
====================

**Fixed:**

* The data folder is now added in the package release.

* The file name render returns the modified documents and the following callbacks use the returned documents instead of the input ones.



v0.6.1
====================

**Added:**

* Add the options `publish` to disable publishing to the proxy.

**Fixed:**

* Fix the "python list doesn't have shape" bug when loading masks in python lists.

* Fix the databroker v2.0 API bugs in tests.



v0.6.0
====================

**Added:**

* Add new callbacks in the `callback` package for the analysis, serialization and visualization for the new data structure from the new xpdacq.

* Add `FileNameRender` to compose file name according to the user's request and put filename in starts and events.

* Add `Analayzer` to process the data to XRD and PDF and save the processed data in the pyFAI standard and pdfgetx standard file and do calbration if necessary.

* Add `DarkSubtraction` to do the dark subtraction of the image in place.

* Add `AnalysisPipeline` that contains the `Analyzer`, `DarkSubtraction` and `Publisher`.

* Add `PlotterBase` as the basic class of the plotters.

* Add `ImagePlotter` to plot the image with or without masks and save image in files.

* Add `WaterfallPlotter` to plot the 1d array in a waterfall plot and save the figure in a file at the end.

* Add `ScalarPlotter` to plot the scalar array as a function of time or other dimensions and save the figure in a file at the end.

* Add `VisualizationPipeline` that contains the `ImagePlotter`, `WaterfallPlotter` and `ScalarPlotter`.

* Add `SerializerBase` as the basic class of the serializers.

* Add `TiffSerializer` to serialize the images in tiff files.

* Add `CSVSerializer` to serialize the scalar data, time stamp and the filename of outputs in csv files.

* Add `YamlSerializer` to serialize the start document in a yaml file using the `safe_dump`.

* Add `NumpySerializer` to serialize the masks in npy files.

* Add `SerializationPipeline` that contians `TiffSerializer`, `CSVSerializer`, `YamlSerializer` and `NumpySerializer`.

**Changed:**

* Make the `callbacks` package contain all the callback classes, including the servers.

* Make the servers able to process the event data from more than one detectors and mutliple different calibrations in one run.

* Make `run_server` command start the analysis, serialization and visualization servers separately in three children processes at the same time.

* Use logging package to stream logs from three processes to `sys.stdout`.

* Change the sections and some keys in the configuration so that users can adjust the `ANALYSIS` section in the configuration using `user_config` key in the start doc.

* Cache the calibration data for the integration and the binners for the masking using `lru_cache`. The cache is valid through the whole session unless it is updated.

* Change the filename pattern of the output files to avoid duplicated file names from different detector images.

* Make the time in the output event streams and the time stamps in the file names the sames as the time in the input event streams. The time that users see will be the same as the time that the data is measured instead of the time that the analysis code runs.

* Allow users to include any measured scalar data in the filename using the `user_config` keyword.

* Allow users to tune whether or not to save the figures, save any kind of data, visualize any kind of data, do the pdfgetx processing or do auto masking.

* Allower users to tune any configuration for auto masking, pyFAI integration and the pdfgetx.

**Deprecated:**

* Deprecate the old callbacks and servers for the old data structure from the old xpdacq.

* Deprecate the dependencies of the suitcase packages.

**Removed:**

* Remove `servers` package and `analyzer` package.

**Fixed:**

* Fix the wrong assignment of the `chi_max` and `chi_argmax`.



v0.5.2
====================

**Fixed:**

* The waterfall plot will be auto scaled after each update and delete.



v0.5.1
====================

**Fixed:**

* The visualization server will clear the plot when the descriptor is received. Before, it clears when the start is received. The plot will remain longer time before the clear.



v0.5.0
====================

**Added:**

* Add `CalibrationExporter`, a callback to export the calibration metadata in poni files.

* Add `xpdvis` server and `xpdsave` server so that the data processing, visualization and exporting can be run in parallel.

* Add `chi_2theta` in the outputs.

* Add yaml metadata output.

**Changed:**

* Data emitted from AnalysisStream changes from numpy objects like numpy.ndarray, numpy.float64 to built-in python objects like list, float.

* Reformat the exported directory structure so that it will be like the outputs from `xpdAn`.

* The format of the output files will be the same as those generated by `xpdAn`.

**Fixed:**

* Fixed the bugs encountered at the 28-ID-1 beamline.



v0.4.7
====================

**Added:**

* Add AreaDetectorTiffHandler for the xpd and lsq servers.

**Changed:**

* The image data can be any array with dimensions N as long as N >= 2. The first N - 2 dimensions will be averaged.

* Simplify the configuration for the servers.

**Deprecated:**

* Deprecate the background subtraction functionality because of the stability.

**Fixed:**

* Use v1 databroker interface for the query of dark images info due to the broken xarray conversion in v2 databroker.

* Fix the bug that server cannot deal with the data for which the background measurement failed.



v0.4.6
====================

**Changed:**

* If there is no "calibration_md" in start document, the server will still process the diffraction image but doesn't do the integration and following step. It will use zero for the results depending on the calibration.

* Move the data processing step to the ``process_data`` method in ``AnalysisStream``.



v0.4.5
====================

**Added:**

* Allow users to use their own mask by adding the file path in the metadata of the run

* Allow users to disable auto masking by using the metadata of the run



v0.4.4
====================

**Added:**

* An xpdvis server that plots figures of analyzed data from xpd server.



v0.4.3
====================

**Added:**

* Add the functionality to export files in xpdan style file structure for the xpd server

* More messages from the server including what is running and the errors from pyFAI calibration

**Changed:**

* Average cli check if the directory exits, make it if not.

* AnalysisStream injects the pdfstream version into the start document.

**Fixed:**

* Fix the bug that the plot setting doesn't work in cli.

* Fix the bug about calibration in xpd server.



v0.4.2
====================

**Fixed:**

* Fix the bug that the background subtraction and dark substrate do not work in the integration



v0.4.1
====================

**Added:**

* The XPD server will publish the data to a proxy

**Changed:**

* The section name of the configuration of XPD server is changed.



v0.4.0
====================

**Added:**

* The base objects to process data from bluesky runs.

* The objects to process the XRD data to PDF data from bluesky runs.

* The functions to replay the analysis.



v0.3.2
====================

**Added:**

* Make callback safe for the Exporter and Visualizer in the XPDRouter.

* Add a DataFrameExporter to export data in dataframe

* Make calibration callback identify special calibrant name 'Ni_calib'

**Changed:**

* Export 1d array in dataframe data instead of the numpy array

* Optimize the layout of figures for visualization callbacks

**Fixed:**

* Fix the bugs of xpd server when it is used with xpdacq.



v0.3.1
====================

**Fixed:**

* Fix the bug that pdfstream has import error if the diffpy.pdfgetx is not in environment



v0.3.0
====================

**Added:**

* `databroker`, `bluesky` are added in the dependencies

* A server to process the streaming x-ray diffraction data to PDF

* A server to decompose processed PDF to a linear combination of other PDFs

* The functions to query the necessary data from the databroker

**Changed:**

* Starting from 0.3.0, the package will be released on `nsls2forge` channel on conda.


v0.2.2
====================

**Changed:**

* Starting from 0.2.2, the package will be released on `diffpy` channel on conda.



v0.2.1
====================



v0.2.0
====================

**Added:**

* `integrate` allows user to supply their own mask

* Add `transform` cli, a simple interface to transform the .chi file to PDF.

* Tutorials for users to use the tools in `pdfstream`.

* `integrate` and `transform` will create the output folder if it does not exists.

**Changed:**

* `load_data` is vended from diffpy. `load_array` accepts `min_rows` and key word arguments.

* `write_out` is renamed to `write_pdfgetter`.

* All the code using `diffpy.pdfgetx` is in the transformation subpackage. Users can choose whether to install the diffpy.pdfgetx.

**Removed:**

* IMPORTANT: modeling, parsers, calibration sub-packages are removed.

* IMPORTANT: remove the dependency on xpdtools



v0.1.3
====================

**Added:**

* Set values and bounds for the variables in the recipe.

**Fixed:**

* Fix the bug that mask is not applied to image in the integration.



v0.1.2
====================

**Added:**

* Add the ``parsers`` that parses the information in FitRecipe to mongo-friendly dictionary.

* Add options in ``multi_phase`` that users can set what parameters they would like to refine.

* Add the function ``create`` to create a recipe based on the data and model.

* Add the function ``initialize`` to populate recipe with variables. Users can choose differnet modes of constraints.

* Add examples for the modeling.

**Changed:**

* CLI ``visualize`` takes list argument ``legends`` instead of string ``legend``. Users can use legends for multiple curves.

**Removed:**

* Remove the codes not frequently used.

**Fixed:**

* Fix bugs in the modeling.



v0.1.1
====================



v0.1.0
====================

**Added:**

* Azimuthal integration of diffraction image with auto masking and background subtraction.

* Calculate the average of multiple diffraction image frames.

* Visualization of pair distribution function (PDF) or other 1D data.

* Visualization of the modeling results of 1D PDF data.

* Easy-to-use tools to create *DiffPy-CMI* recipe to model PDF and run optimization.

* Simple csv-file-based database to save the modeling results.

* A command line interface (CLI) for all the functionality.
