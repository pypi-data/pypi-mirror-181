# Hazelbean
A collection of geospatial processing tools based on gdal, numpy, scipy, cython, pygeoprocessing, taskgraph, natcap.invest, geopandas and many others to assist in common spatial analysis tasks in sustainability science, ecosystem service assessment, global integrated modelling assessment,  natural capital accounting, and/or calculable general equilibrium modelling.

Hazelbean started as a personal research package of scripts for Justin Johnson and is not supported for broad release. However, hazelbean underlies several experimental software releases, including some from the Natural Capital Project, and thus it is available via "pip install hazelbean". Note that hazelbean only provides a Python 3.6, 64 bit, Windows version, however with the exception of precompiled cython files, it should be cross-platform and cross-version. The precompiled files are only loaded as needed.


## Installation

Pip installing Hazelbean will attempt to install required libraries, but many of these must be compiled for your computer. You can solve each one manually for your chosen opperating system, or you can use these Anaconda-based steps here:

- Install Anaconda3 with the newest python version (tested at python 3.6.3)
- Ensure you have the latest conda using 
```conda update -n base conda```
- Create a new conda environment using
```conda create --name env_name```
- Activate the environment with 
```conda activate env_name```
- Install libraries using conda command: 
```conda install -c conda-forge natcap.invest geopandas rasterstats netCDF4 cartopy xlrd markdown qtpy qtawesome plotly descartes pygeoprocessing taskgraph cython rioxarray dask google-cloud-datastore google-cloud-storage aenum anytree statsmodels openpyxl seaborn twine pyqt ipykernel imageio```
- And then finally, install hazelbean via pip:
```pip install hazelbean```

## Numpy errors

If numpy throws "wrong size or changes size binary": upgrade numpy at the end of the installation process. See for details: https://stackoverflow.com/questions/66060487/valueerror-numpy-ndarray-size-changed-may-indicate-binary-incompatibility-exp

# Mac specific errors

Your python environment has to have permissions to access and write to the base data folder.

## More information
See the author's personal webpage, https://justinandrewjohnson.com/ for more details about the underlying research.

## Project Flow

One key component of Hazelbean is that it manages directories, base_data, etc. using a concept called ProjectFlow. ProjectFlow defines a tree of tasks that can easily be run in parallel where needed and keeping track of task-dependencies. ProjectFlow borrows heavily in concept (though not in code) from the task_graph library produced by Rich Sharp but adds a predefined file structure suited to research and exploration tasks. 

### Project Flow notes

Project Flow is intended to flow easily into the situation where you have coded a script that grows and grows until you think "oops, I should really make this modular." Thus, it has several modalities useful to researchers ranging from simple drop-in solution to complex scripting framework.

#### Notes

In run.py, initialize the project flow object. This is the only place where user supplied (possibly absolute but can be relative) path is stated. The p ProjectFlow object is the one global variable used throughout all parts of hazelbean.

```python
import hazelbean as hb

if __name__ == '__main__':
    p = hb.ProjectFlow(r'C:\Files\Research\cge\gtap_invest\projects\feedback_policies_and_tipping_points')
```

In a multi-file setup, in the run.py you will need to import different scripts, such as main.py i.e.:
```python
import visualizations.main
```

The script file mainpy can have whatever code, but in particular can include "task" functions. A task function, shown below, takes only p as an agrument and returns p (potentially modified). It also must have a conditional (if p.run_this:) to specify what always runs (and is assumed to run trivially fast, i.e., to specify file paths) just by nature of having it in the task tree and what is run only conditionally (based on the task.run attribute, or optionally based on satisfying a completed function.)
```python
def example_task_function(p):
    """Fast function that creates several tiny geotiffs of gaussian-like kernels for later use in ffn_convolve."""

    if p.run_this:
        for i in computationally_intensive_loop:
            print(i)
```
**Important Non-Obvious Note**

Importing the script will define function(s) to add "tasks", which take the ProjectFlow object as an argument and returns it after potential modification. 

```python
def add_all_tasks_to_task_tree(p):
    p.generated_kernels_task = p.add_task(example_task_function)
```



