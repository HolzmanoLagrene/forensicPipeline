#!/bin/bash

docker run --rm -it --mount src="$(pwd)"/notebooks,dst=/notebooks,type=bind\
 --mount src="$(pwd)"/code_snippets,dst=/home/jovyan/.jupyter/lab/user-settings/jupyterlab-code-snippets/,type=bind\
  -p 8888:8888 notebook_experiment jupyter lab --ip='*' --port=8888 --no-browser --NotebookApp.token='' --allow-root --notebook-dir=/notebooks
