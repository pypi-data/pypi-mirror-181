from .reporter import Reporter, ReporterConnectionDetails
from ..utils.message import get_message_formatter
from eputils.thread.publisher import PublisherThread
from queue import SimpleQueue
from logging import Logger
import os

class AMTQReporter(Reporter):
    """Reports status updates to algorithm manager
    using AMTQ"""
    def __init__(self, logger: Logger, connection_details: ReporterConnectionDetails) -> None:
        super().__init__(logger)
        self.publish_queue = SimpleQueue()
        self.publisher_thread = PublisherThread(
            host=connection_details.host,
            creds_provider=connection_details.creds_provider,
            exchange=connection_details.messagebus.status_update_exchange,
            publish_queue=self.publish_queue,
            app_id=f"{connection_details.messagebus.app_id}.publisher",
            logger=logger)
        
    
    def report(self, message):
        self._print("Publishing "+ message)
        self.publish_queue.put((message, self._context.messagebus.status_update_routing))
        self._print("Published message")
        return True
    
    def __enter__(self):
        self.publisher_thread.start()
        return self
    
    def __exit__(self, type, value, tb):
        self.publisher_thread.stop()
        return super().__exit__(type, value, tb)

class PreprocessAMTQReporter(AMTQReporter):
    def __init__(self, logger: Logger, connection_details: ReporterConnectionDetails) -> None:
        super().__init__(logger, connection_details)
        self.message_formatter = get_message_formatter()

    def report(self, message):
        if self.publisher_thread is None:
            raise Exception("Not connected to RabbitMQ, call connect() first!")
        if "EP_ALGORITHM_SUB_JOB_REFERENCE" not in os.environ:
            raise Exception("Sub job reference not present in environment")
        if not self.publisher_thread.is_alive():
            raise Exception("Thread is not alive")
        if not self.publisher_thread.is_connected():
            raise Exception("Thread not connected to broker")

        sub_job_reference = os.environ["EP_ALGORITHM_SUB_JOB_REFERENCE"]

        processed_message = self.message_formatter.get_message(sub_job_reference, "busy", message)

        return super().report(processed_message)

    def __enter__(self):
        return super().__enter__()
    
    def __exit__(self, type, value, tb):
        return super().__exit__(type, value, tb)