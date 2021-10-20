import os
import shutil

import docker
from django.conf import settings

from docker_api import api_settings


def __prepare_case_folders__(evidence_path):
    if not os.path.isdir(os.path.join(evidence_path, "plaso")):
        os.makedirs(os.path.join(evidence_path, "plaso"))
    else:
        pass
    if not os.path.isdir(os.path.join(evidence_path, "logs")):
        os.makedirs(os.path.join(evidence_path, "logs"))
    else:
        pass


def __print_logs(container, evidence_name, type, verbose):
    evidence_path = os.path.join(settings.EVIDENCE_DIR, evidence_name, "logs")
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
    worker_case_path = os.path.join(settings.EVIDENCE_DIR, evidence_name)
    docker_case_path = os.path.join(settings.DOCKER_EVIDENCE_DIR, evidence_name)

    if command == "log2timeline":
        __prepare_case_folders__(worker_case_path)
        command_string = f"log2timeline \
                                     --storage_file {docker_case_path}/plaso/storage.plaso\
                                     --logfile {docker_case_path}/logs/log2timeline.log \
                                      --status_view linear\
                                      -d\
                                      {docker_case_path}/evidence"
    elif command == "pinfo":
        command_string = f"pinfo \
                                                          -w {docker_case_path}/plaso/pinfo.json \
                                                          -v \
                                                          --output_format json \
                                                          {docker_case_path}/plaso/storage.plaso"
    elif command == "psort":
        command_string = f"psort \
                                                        -d \
                                                --logfile {docker_case_path}/logs/psort.log \
                                                -o elastic \
                                                --status_view linear\
                                                --elastic_mappings /usr/share/plaso/elasticsearch.mappings\
                                                --server {settings.ELASTIC_HOST}\
                                                --port {settings.ELASTIC_PORT}\
                                                --index_name plaso_{evidence_name}\
                                                        {docker_case_path}/plaso/storage.plaso"
    else:
        raise Exception("Unknown command type")

    container = docker.from_env().containers.run(settings.DOCKER_PLASO_CONTAINER_NAME,
                                                 command_string,
                                                 auto_remove=False,
                                                 detach=True,
                                                 network_mode="host",
                                                 name=command + "_" + evidence_name,
                                                 volumes={settings.DOCKER_VOLUME_EVIDENCE:
                                                              {'bind': settings.DOCKER_EVIDENCE_DIR, 'mode': 'rw'},
                                                          }
                                                 )

    print(f'Starting container {container.name} (ID: {container.id})', end='')
    print(f'Celery worker case path: {worker_case_path}', end='')
    print(f'Docker case path: {docker_case_path}', end='')

    print(f'Waiting for {container.name} to finish', end='')
    result = container.wait()

    print(f'{container.name} logs: {container.logs()}')

    print(f'Removing {container.name}', end='')
    container.remove()

    return result


def prepare_jupyter_notebook(evidence_name):
    notebook_path = os.path.join(api_settings.NOTEBOOK_PATH, evidence_name)
    default_notebook_path = os.path.join(api_settings.NOTEBOOK_PATH, "default", "default.ipynb")
    shutil.copy(default_notebook_path, notebook_path)


def run_jupyter_notebook(evidence_name):
    notebook_path = os.path.join(api_settings.NOTEBOOK_PATH, evidence_name)
    prepare_jupyter_notebook(evidence_name)
    command_string = f"jupyter lab --ip='*'\
                        --port=8888\
                         --no-browser\
                          --NotebookApp.token=''\
                           --allow-root\
                            --notebook-dir=/notebooks"
    container = docker.from_env().containers.run(settings.DOCKER_NOTEBOOK_CONTAINER_NAME,
                                                 command_string,
                                                 auto_remove=True,
                                                 detach=True,
                                                 ports={8888: 8888},
                                                 name="jupyterlab_" + evidence_name,
                                                 volumes={notebook_path:
                                                              {'bind': '/notebooks', 'mode': 'rw'},
                                                          api_settings.SNIPPETS_PATH:
                                                              {
                                                                  'bind': '/home/jovyan/.jupyter/lab/user-settings/jupyterlab-code-snippets/',
                                                                  'mode': 'rw'}
                                                          }
                                                 )
    result = container.wait()
    return result


def run_log2timeline(evidence_name):
    try:
        result = run_docker_container("log2timeline", evidence_name)
        return result["StatusCode"]

    except Exception as ex:
        print(f'Exception: {ex}')
        return -99


def run_pinfo(evidence_name):
    try:
        result = run_docker_container("pinfo", evidence_name)
        return result["StatusCode"]

    except Exception as ex:
        print(f'Exception: {ex}')
        return -99


def run_psort(evidence_name):
    try:
        result = run_docker_container("psort", evidence_name)
        return result["StatusCode"]

    except Exception as ex:
        print(f'Exception: {ex}')
        return -99
