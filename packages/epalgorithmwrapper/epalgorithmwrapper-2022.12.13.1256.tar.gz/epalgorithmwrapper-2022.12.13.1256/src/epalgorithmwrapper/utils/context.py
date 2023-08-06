from logging import Logger
from threading import Thread
from .manifest import Manifest
from .input_provider import InputProvider
from ..dataprovider.dataprovider import DataProvider
from ..datauploader.datauploader import DataUploader

class ConnectionContext:
    def __init__(self,
                 host,
                 host_filesystem,
                 host_algorithm_manager,
                 creds_provider) -> None:
        self.host: str = host
        self.host_filesystem: str = host_filesystem
        self.host_algorithm_manager: str = host_algorithm_manager
        self.creds_provider = creds_provider

class MessagebusContext:
    def __init__(self,
                 app_id,
                 job_queue_name,
                 status_update_exchange,
                 status_update_routing) -> None:
        self.app_id = app_id
        self.job_queue_name = job_queue_name
        self.status_update_exchange = status_update_exchange
        self.status_update_routing = status_update_routing

class Context:
    def __init__(self, 
                 connection,
                 messagebus,
                 logger, 
                 manifest,
                 configuration,
                 input_provider,
                 data_provider,
                 data_uploader) -> None:
        self.input_provider: InputProvider = input_provider
        self.threads: list[Thread] = []
        self.connection: ConnectionContext = connection
        self.messagebus: MessagebusContext = messagebus
        self.logger: Logger = logger
        self.manifest: Manifest = manifest
        self.configuration = configuration
        self.data_provider: DataProvider = data_provider
        self.data_uploader: DataUploader = data_uploader

    def add_thread(self, thread: Thread):
        self.threads += [thread]

    def stop_threads(self):
        for t in self.threads:
            t.stop()