import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH= os.path.join(BASE_PATH,"uploads")
PLASO_CONTAINER_NAME = "plaso:latest"

elasticsearch_server="localhost"
elasticsearch_port=9200