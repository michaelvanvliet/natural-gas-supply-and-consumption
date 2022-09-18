FROM jupyter/minimal-notebook
ADD requirements.txt /
RUN pip install -r /requirements.txt
ADD analyse.ipynb /home/jovyan/
CMD [ "jupyter", "notebook" ]