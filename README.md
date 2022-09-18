**PLEASE NOTE! THIS NOTEBOOK IS STILL WORK IN PROGRESS!**

# NATURAL GAS
In the last few years prices of natural resources, such as gas, have skyrocketed. The impact in the Netherlands, as in many other countries, is huge and therefore a good subject to use for a new data science project! We will be exploring historic data to try and understand what is happening and try to explain what decisions and changes have led to where we are now.

## DATA
In the Netherlands we have the Central Bureau of Statistics ([CBS](https://www.cbs.nl)). They provide insights into many topics such as unemployment rates, greenhouse gas emissions, inflation, house pricing, supply and demand of natural gas, and many more. In addition to writing very informative articles (based on facts), they also give open access to the data used for the articles, such as this one: [Natural gas consumption 25 percent lower in first half of 2022](https://www.cbs.nl/en-gb/news/2022/35/natural-gas-consumption-25-percent-lower-in-first-half-of-2022) ([link to data](https://opendata.cbs.nl/statline/portal.html?_la=en&_catalog=CBS&tableId=00372eng&_theme=1053)).

## TOOLS
For this project we will be making use of [Python](https://www.python.org/), [Jupyter](https://jupyter.org/), [Pandas](https://pandas.pydata.org/), [Matplotlib](https://matplotlib.org/), [Seaborn](https://seaborn.pydata.org/), and [many more](https://pypi.org/). A full list can be found in the requirements.txt file of the [repository](https://github.com/michaelvanvliet/natural-gas-supply-and-consumption)

## GETTING STARTED

### 1. MYBINDER (easiest)
Simply click the link below and wait until the browser opens the notebook for you. No downloading or setup needed, simply instantiate it using this free awesome service called MyBinder.
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/michaelvanvliet/natural-gas-supply-and-consumption/HEAD?urlpath=notebooks/analyse.ipynb)

### 2. LOCAL DOCKER SETUP (requires Docker to be installed)
After installing [Docker](https://www.docker.com/) you run the following commands:

```
docker build -t natural-gas-supply-and-consumption .
docker run -it --rm -p 8888:8888  natural-gas-supply-and-consumption
```

The first command should download the required container image and add the requirement for this notebook (see Dockerfile). The second command is the start the container you just build. More information on the base container used and how to interact with it can be found here: [Jupyter Docker Stacks](https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html)
After a few seconds you should see someting like this:
```
[I 19:05:08.387 NotebookApp] Jupyter Notebook 6.4.12 is running at:
[I 19:05:08.387 NotebookApp] http://7ba75e1cd772:8888/?token=8cd3809dd87a580a1d91052fa078325597db60cdfcc3d189
[I 19:05:08.387 NotebookApp]  or http://127.0.0.1:8888/?token=8cd3809dd87a580a1d91052fa078325597db60cdfcc3d189
[I 19:05:08.387 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 19:05:08.388 NotebookApp] 
    
    To access the notebook, open this file in a browser:
        file:///home/jovyan/.local/share/jupyter/runtime/nbserver-7-open.html
    Or copy and paste one of these URLs:
        http://7ba75e1cd772:8888/?token=8cd3809dd87a580a1d91052fa078325597db60cdfcc3d189
     or http://127.0.0.1:8888/?token=8cd3809dd87a580a1d91052fa078325597db60cdfcc3d189
```
Now best you can do is open the last URL that starts with http://127.0.0.1:8888/?token=xxx, this will take you to the root of the notebook where you can select the notebook **analyse.ipynb**

If this fails, and you are sure you want to use Docker, check the manual at [docs.docker.com](https://docs.docker.com/)

### 3. LOCAL INSTALLATION (advanced)
Clone (using Git) or just download the repository to the preferred location on your system. Make sure the latest version of [Python](https://www.python.org/) has been installed on your system. I recommend setting up a [virtual environment](https://docs.python.org/3/tutorial/venv.html) to manage the dependencies for this project only, and not end up having conflicting dependecies with other projects. A great cross-platform IDE (tool to edit and run the code) is VSCode ([Windows](https://learn.microsoft.com/en-us/windows/python/beginners)), especially for less experienced coders a good place to start. Install the required libraries using Python PIP library and point to the [requirements.txt](https://pip.pypa.io/en/stable/getting-started/#install-multiple-packages-using-a-requirements-file) file of the repository. Now that all requirements have been installed you can simply start the notebook with the following [instructions](https://jupyter.org/install).

```
jupyter notebook
```

## DISCLAIMER
All information in this document and the notebook(s) is based on my own opinion and I'm not an expert on natural gas production and/or consumption!