import os

import docker
from docker.errors import APIError, ContainerError, ImageNotFound

from plaso_api import api_settings


def __fix_folder_configuration(evidence_path):
    if not os.path.isdir(os.path.join(evidence_path, "plaso")):
        os.makedirs(os.path.join(evidence_path, "plaso"))
    else:
        pass
    if not os.path.isdir(os.path.join(evidence_path, "logs")):
        os.makedirs(os.path.join(evidence_path, "logs"))
    else:
        pass


def __print_logs(container, evidence_name, type, verbose):
    evidence_path = os.path.join(api_settings.DATA_PATH, evidence_name, "logs")
    log_path = os.path.join(evidence_path, f"{type}_plaso_logs.log")
    logs = container.logs(stream=True, follow=True)
    try:
        while True:
            line = next(logs).decode("utf-8")
            if verbose:
                print(line, end="")
            with open(log_path, "a+") as out_:
                out_.write(line)
    except StopIteration:
        print(f'log stream ended for container {container.name}')


def stop_process(evidence_name):
    for container in docker.from_env().containers.list():
        if container.name.endswith(evidence_name):
            container.stop()


def run_docker_container(command, evidence_name):
    evidence_path = os.path.join(api_settings.DATA_PATH, evidence_name)
    if command == "log2timeline":
        __fix_folder_configuration(evidence_path)
        command_string = "log2timeline \
                                     --storage_file /data/plaso/storage.plaso\
                                     --logfile /data/logs/log2timeline.log \
                                      --status_view linear\
                                      -d \
                                      /data/evidence"
    elif command == "pinfo":
        command_string = "pinfo \
                                                          -w /data/plaso/pinfo.json \
                                                          -v \
                                                          --output_format json \
                                                          /data/plaso/storage.plaso"
    elif command == "psort":
        command_string = f"psort \
                                                        -d \
                                                --logfile /data/logs/psort.log \
                                                -o elastic \
                                                --status_view linear\
                                                --elastic_mappings /usr/share/plaso/elasticsearch.mappings\
                                                --server {api_settings.elasticsearch_server}\
                                                --port {api_settings.elasticsearch_port}\
                                                --index_name plaso_{evidence_name}\
                                                        /data/plaso/storage.plaso"
    else:
        raise Exception("Unknown command type")

    container = docker.from_env().containers.run(api_settings.PLASO_CONTAINER_NAME,
                                                 command_string,
                                                 auto_remove=True,
                                                 detach=True,
                                                 network_mode="host",
                                                 name=command + "_" + evidence_name,
                                                 volumes={evidence_path:
                                                              {'bind': '/data', 'mode': 'rw'},
                                                          }
                                                 )
    result = container.wait()
    return result


def run_log2timeline(evidence_name):
    try:
        result = run_docker_container("log2timeline", evidence_name)
    except APIError as api_error:
        return -99
    except ContainerError as cont_error:
        return -99
    except ImageNotFound as img_error:
        return -99
    except Exception as ex:
        return -99


def run_pinfo(evidence_name):
    try:
        result = run_docker_container("pinfo", evidence_name)
    except APIError as api_error:
        return -99
    except ContainerError as cont_error:
        return -99
    except ImageNotFound as img_error:
        return -99
    except Exception as ex:
        return -99


def run_psort(evidence_name):
    try:
        result = run_docker_container("psort", evidence_name)
        return result["StatusCode"]
    except APIError as api_error:
        return -99
    except ContainerError as cont_error:
        return -99
    except ImageNotFound as img_error:
        return -99
    except Exception as ex:
        return -99
