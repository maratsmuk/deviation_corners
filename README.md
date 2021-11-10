# Generation of plots for the ``Deviation of corners'' project
## Created by M.S. Mukhametzhanov
### Given deviations of floor vs ceiling corners of a model with ground truth labels for the room name and number of corners in that room with predictions.
### Aim: to create meaningful statistics of how well the model performed.

Contents: 
- myplotlib.py: the main class for creation of pictures
- myplotlib_utest.py: the unit tests for checking its correctness
- requirements.txt: the requirements file
- venv/ : the virtual environment folder created by Pycharm
- plots/ : the main folder with the plots. There are subfolders for the scatter plots, boxplots and histplots.
- deviation_corners.ipynb: the Jupyter notebook for calling the created class and studying the results 

myplotlib.py usage: 

``#import myplotlib as mpl``

``newpl = mpl.plotlib()``
``path = newpl.draw_plots(json_name, kind)``

``json_name`` is the link to the json file with the dataframe (local or remote), ``kind`` is the type of the plot:
- ``conf`` for confidence matrix
- ``corr`` for correlation matrix for all numeric columns
- ``roc`` for the Receiver Operating Characteristic (extended for the multiclass case)
- ``scatter`` for the scatter plots for each column vs each other column (single scatter plots for each columnn are also included)
- ``boxplot`` for boxplots of each column (separated by classes)
- ``hisplot`` for creating histograms for each column (separated by classes)
- ``hist`` for creating histograms for target discrete variables only.

The set of paths to each generated plot is returned in ``path``. The paths to all created-so-far plots are also saved in the ``newpl.plot_paths`` (implemented as a python set).
Call ``newpl.clear()`` to clear all the contents of the ``newpl`` (e.g., the paths to created-so-far plots). The plots in the respective paths are not deleted in this case. 

