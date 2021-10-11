import asyncio
import os
import threading

import docker

from . import api_settings


class DockerHandler:
    def __init__(self):
        self.client = docker.from_env()

    @staticmethod
    def __check_folder_configuration(evidence_name):
        status = True
        evidence_path = os.path.join(api_settings.DATA_PATH, evidence_name)
        if os.path.isdir(evidence_path):
            if os.path.isdir(os.path.join(evidence_path, "evidences")):
                pass
            else:
                print(f"No such directory {os.path.isdir(os.path.join(evidence_path, 'evidences'))}. Exiting.")
                status = False
            if not os.path.isdir(os.path.join(evidence_path, "plaso")):
                os.makedirs(os.path.join(evidence_path, "plaso"))
            else:
                pass
            if not os.path.isdir(os.path.join(evidence_path, "logs")):
                os.makedirs(os.path.join(evidence_path, "logs"))
            else:
                pass
        else:
            print(f"No such directory {evidence_path}. Exiting.")
            status = False
        return status

    @staticmethod
    def __print_logs_in_thread(container, evidence_name, type, verbose):
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

    def __print_logs(self, container, evidence_name, type, verbose, background=False):
        if background:
            thread = threading.Thread(target=self.__print_logs_in_thread, args=(container, evidence_name, type, verbose))
            thread.daemon = True  # Daemonize thread
            thread.start()
        else:
            self.__print_logs_in_thread(container, evidence_name, type, verbose)

    def stop_process(self, evidence_name):
        for container in self.client.containers.list():
            if container.name.endswith(evidence_name):
                container.stop()

    async def run_log2timeline(self, evidence_name, verbose=False):
        folder_config_ok = self.__check_folder_configuration(evidence_name)
        if folder_config_ok:
            evidence_path = os.path.join(api_settings.DATA_PATH, evidence_name)
            container = self.client.containers.run(api_settings.PLASO_CONTAINER_NAME,
                                                   f"log2timeline \
                                                   --storage_file /data/plaso/storage.plaso\
                                                    --logfile /data/logs/log2timeline.log \
                                                    --status_view linear\
                                                    -d \
                                                    /data/evidences",
                                                   auto_remove=True,
                                                   detach=True,
                                                   name="log2timeline" + "_" + evidence_name,
                                                   volumes={evidence_path:
                                                                {'bind': '/data', 'mode': 'rw'},
                                                            }
                                                   )
            awaitable = asyncio.to_thread(container.wait)
            result = await awaitable
            return result['StatusCode']

    async def run_pinfo(self, evidence_name, verbose=False):
        evidence_path = os.path.join(api_settings.DATA_PATH, evidence_name)
        container = self.client.containers.run(api_settings.PLASO_CONTAINER_NAME,
                                               f"pinfo \
                                                        -w /data/plaso/pinfo.json \
                                                        -v \
                                                        --output_format json \
                                                        /data/plaso/storage.plaso",
                                               auto_remove=True,
                                               detach=True,
                                               name="pinfo" + "_" + evidence_name,
                                               volumes={evidence_path:
                                                            {'bind': '/data', 'mode': 'rw'},
                                                        }
                                               )
        awaitable = asyncio.to_thread(container.wait)
        result = await awaitable
        return result['StatusCode']

    async def run_psort(self, evidence_name, verbose=False):
        evidence_path = os.path.join(api_settings.DATA_PATH, evidence_name)
        container = self.client.containers.run(api_settings.PLASO_CONTAINER_NAME,
                                               f"psort \
                                                        -d \
                                                --logfile /data/logs/psort.log \
                                                -o elastic \
                                                --status_view linear\
                                                --elastic_mappings /usr/share/plaso/elasticsearch.mappings\
                                                --server {api_settings.elasticsearch_server}\
                                                --port {api_settings.elasticsearch_port}\
                                                --index_name plaso_{evidence_name}\
                                                        /data/plaso/storage.plaso",
                                               auto_remove=True,
                                               detach=True,
                                               network_mode="host",
                                               name="psort" + "_" + evidence_name,
                                               volumes={evidence_path:
                                                            {'bind': '/data', 'mode': 'rw'},
                                                        }
                                               )
        awaitable = asyncio.to_thread(container.wait)
        result = await awaitable
        return result['StatusCode']
