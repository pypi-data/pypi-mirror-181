from ..utils.filesystem_utils import get_file_contents
from ..utils.configuration import Configuration

class Report:
    class Status:
        FAILURE = "FAILURE"
        SUCCESS = "SUCCESS"

    REPORT_LOCATION = Configuration.get_configuration()[Configuration.Key.OUTPUT_REPORT_LOCATION]
    TEMPLATE_LOCATION = Configuration.get_configuration()[Configuration.Key.REPORT_TEMPLATE_LOCATION]

    @staticmethod
    def __get_report_template():
        return get_file_contents(Report.TEMPLATE_LOCATION)

    @staticmethod
    def __save_report(report, path):
        with open(path, 'w+') as f:
            f.write(report)

    @staticmethod
    def write_report(status: Status):
        template = Report.__get_report_template()
        report = template.format(status=status)
        Report.__save_report(report, Report.REPORT_LOCATION)
