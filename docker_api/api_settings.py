import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_PATH, "uploads")
NOTEBOOK_PATH = os.path.join(BASE_PATH, "jupyterlab", "notebooks")
SNIPPETS_PATH = os.path.join(BASE_PATH, "jupyterlab", "snippets")
PLASO_CONTAINER_NAME = "plaso:latest"
NOTEBOOK_CONTAINER_NAME = "notebook:latest"

elasticsearch_server = "localhost"
elasticsearch_port = 9200
