from .rest_api_reporter import RESTAPIReporter, PreprocessRESTAPIReporter, VoidReporter
from .reporter import Reporter
from ..utils.input_provider import InputProvider

def get_reporter(host, logger, input_provider: InputProvider) -> Reporter:
    if input_provider is not None and input_provider.skip_reports():
        return VoidReporter(logger)
    return RESTAPIReporter(host, logger)

def get_preprocess_reporter(host, logger, input_provider: InputProvider) -> Reporter:
    if input_provider is not None and input_provider.skip_reports():
        return VoidReporter(logger)
    return PreprocessRESTAPIReporter(host, logger)