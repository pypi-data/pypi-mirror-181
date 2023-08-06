from .datauploader import DataUploader, HTTPDataUploader, VoidUploader
import logging

def get_datauploader(host: str, logger: logging.Logger, local=False) -> DataUploader:
    upload_url = f"http://{host}"
    if local:
        logger.warning("Using void data upload instead of HTTP uploader")
        return VoidUploader(logger)
    logger.info("Using normal data uploader")
    return HTTPDataUploader(upload_url, logger)