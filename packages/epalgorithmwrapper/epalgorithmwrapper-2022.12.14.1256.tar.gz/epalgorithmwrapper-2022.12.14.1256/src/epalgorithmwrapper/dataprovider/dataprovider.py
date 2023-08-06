import logging
from ..utils.http_tools import send_post

class DataProvider:
    def send_request(self, request_body):
        """Send a request with a certain body"""
    
class HTTPDataProvider(DataProvider):
    def __init__(self, download_url: str, logger: logging.Logger) -> None:
        self.download_url = download_url
        self.logger = logger
    
    def send_request(self, request_body):
        self.logger.info("Sending request..")
        r = send_post(self.download_url, request_body, self.logger)

        if r is None or not r.ok:
            self.logger.error(f"!Could not download resource: {request_body}")
            return None
        
        self.logger.info("Received data")
        return r.content

class LocalFileProvider(DataProvider):
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger

    def send_request(self, request_body):
        self.logger.info("Using local file instead of downloading")
        return True # File is already available
