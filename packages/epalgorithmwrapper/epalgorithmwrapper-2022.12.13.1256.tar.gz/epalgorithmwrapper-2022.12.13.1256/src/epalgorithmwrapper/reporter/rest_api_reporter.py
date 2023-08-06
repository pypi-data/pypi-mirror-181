from .reporter import Reporter
from ..utils.http_tools import send_post_raw
from ..utils.message import get_message_formatter
from logging import Logger
import os

class RESTAPIReporter(Reporter):
    def __init__(self, 
            host: str,
            logger: Logger,
            route: str = "status-update") -> None:
        super().__init__(logger)
        self.host = host
        self.route = route
        self.report_url = f"http://{self.host}/{self.route}"
    
    def report(self, message) -> bool:
        url = self.report_url
        data = message
        self._print("Sending Rest POST Report")
        r = send_post_raw(url, data, self._logger, {"Content-Type": "application/json"})
        if r is not None:
            self._print("Sent Rest POST Report!")
            return True
        self._print("Failed Rest POST Report")
        return False

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, tb):
        return super().__exit__(type, value, tb)

class PreprocessRESTAPIReporter(RESTAPIReporter):
    def __init__(self, 
            host: str,
            logger: Logger) -> None:
        super().__init__(host, logger)

        self.message_formatter = get_message_formatter()
    
    def report(self, message) -> bool:
        if "EP_ALGORITHM_SUB_JOB_REFERENCE" not in os.environ:
            raise Exception("Sub job reference not present in environment")

        sub_job_reference = os.environ["EP_ALGORITHM_SUB_JOB_REFERENCE"]

        processed_message = self.message_formatter.get_message(sub_job_reference, "busy", message)
        return super().report(processed_message)

    def __enter__(self):
        return super().__enter__()
    
    def __exit__(self, type, value, tb):
        return super().__exit__(type, value, tb)

class VoidReporter(Reporter):
    def report(self, message: str):
        return True
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, tb):
        return super().__exit__(type, value, tb)