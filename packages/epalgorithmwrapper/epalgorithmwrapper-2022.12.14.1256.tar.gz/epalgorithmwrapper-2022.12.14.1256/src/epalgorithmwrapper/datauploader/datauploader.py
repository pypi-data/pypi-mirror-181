import logging
from ..utils.http_tools import send_post_file
from ..utils.filesystem_utils import file_exists

class DataUploader:
    def send_request(self, patient_id, case_id, file_context, workdir, filename) -> bool:
        pass

class HTTPDataUploader(DataUploader):
    def __init__(self, upload_url: str, logger: logging.Logger) -> None:
        self.upload_url = upload_url
        self.logger = logger
    
    def send_request(self, patient_id, case_id, file_context, workdir, filename) -> bool:
        url = f"{self.upload_url}/upload/{patient_id}/{case_id}/{file_context}"
        resource_location = workdir+"/"+filename
        if not file_exists(resource_location): 
            self.logger.error(f"File {resource_location} does not exist")
            return False

        self.logger.info("Sending file post request..")
        r = send_post_file(url, resource_location, self.logger)
        self.logger.info("Posted file")

        return True

class VoidUploader(DataUploader):
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger
    
    def send_request(self, patient_id, case_id, file_context, workdir, filename) -> bool:
        self.logger.info("Uploading file to void (so not uploading)")
        return True