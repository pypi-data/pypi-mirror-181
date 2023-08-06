import os
from queue import Queue
import logging

from .utils.manifest import Manifest
from .utils.configuration import Configuration
from .utils.context import Context, ConnectionContext, MessagebusContext
from .jobprovider.job_provider_factory import get_job_provider
from .jobprovider.message_processor import JsonV1Processor
from .jobprovider.resource_manager import get_resource_manager
from .connection import get_messagebroker_host, get_filesystem_host, get_creds_provider, get_algorithm_manager_host
from .utils.input_provider import InputProvider
from .dataprovider.dataprovider_factory import get_dataprovider
from .datauploader.datauploader_factory import get_datauploader

context = None
job_provider = None
publish_queue = None

def decorated_print(header, message):
    return f"{header}: {message}"

def start(logger: logging.Logger, input_provider: InputProvider):
    is_development = input_provider.is_development_mode()
    local_data_mode = input_provider.skip_download_upload()
    logger.warning(f"Development mode: {is_development}")

    host_messagebroker = get_messagebroker_host()
    host_filesystem = get_filesystem_host()
    host_algorithm_manager = get_algorithm_manager_host()

    logger.info(f"Using host messagebroker {host_messagebroker}")
    logger.info(f"Using host filesystem {host_filesystem}")

    data_provider = get_dataprovider(host_filesystem, logger, local_data_mode)
    data_uploader = get_datauploader(host_filesystem, logger, local_data_mode)
    
    creds_provider = get_creds_provider()
    configuration = Configuration.get_configuration()
    manifest = Manifest.get_manifest(is_development)

    connection = ConnectionContext(host_messagebroker, 
                                   host_filesystem,
                                   host_algorithm_manager,
                                   creds_provider)
    messagebus = MessagebusContext(app_id=f"algorithm.{manifest[Manifest.Key.IDENTIFIER]}", 
                                   job_queue_name=manifest[Manifest.Key.IDENTIFIER],
                                   status_update_exchange=configuration[Configuration.Key.RABBITMQ_STATUS_UPDATE_EXCHANGE], 
                                   status_update_routing=configuration[Configuration.Key.RABBITMQ_STATUS_UPDATE_ROUTING])
    context = Context(connection,
                      messagebus,
                      logger, 
                      manifest,
                      configuration,
                      input_provider,
                      data_provider,
                      data_uploader)

    logger.info(decorated_print("Manifest", manifest))
    logger.info(decorated_print("Configuration", configuration))

    resource_manager = get_resource_manager(context)
    message_processor = JsonV1Processor(context, resource_manager)
    get_job_provider(input_provider, context, message_processor)

def get_publish_queue() -> Queue:
    return publish_queue

def get_context() -> Context:
    return context