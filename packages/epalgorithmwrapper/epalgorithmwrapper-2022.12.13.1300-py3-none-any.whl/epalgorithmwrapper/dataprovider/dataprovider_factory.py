from .dataprovider import DataProvider, HTTPDataProvider, LocalFileProvider
import logging

def get_dataprovider(host: str, logger: logging.Logger, local=False) -> DataProvider:
    if local:
        logger.warning("Using local data provider instead of HTTP provider")
        return __get_local_dataprovider(logger)
    logger.info("Using normal data provider")
    return __get_http_dataprovider(host, logger)

def __get_http_dataprovider(host: str, logger: logging.Logger):
    url = f"http://{host}"
    download_url = f"{url}/download"
    return HTTPDataProvider(download_url, logger)

def __get_local_dataprovider(logger: logging.Logger):
    return LocalFileProvider(logger)