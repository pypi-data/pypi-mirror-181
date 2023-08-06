from ..utils.manifest import Manifest
from ..utils.configuration import Configuration
from ..utils.cli_tools import dispatch_command
from ..utils.context import Context
from ..utils.filesystem_utils import clear_folder, get_file_contents
from ..utils.message import get_message_formatter
from ..reporter.reporter_factory import get_reporter
from .instruction import JobInstruction
from .resource_manager import ResourceManager
import os

class MessageProcessor:
    def process(self, instruction: JobInstruction):
        """Process message with self-defined logic"""

class JsonV1Processor(MessageProcessor):
    def __init__(self, context: Context, resource_manager: ResourceManager) -> None:
        self.resource_manager = resource_manager
        self._logger = context.logger
        self._context = context
        self._message_formatter = get_message_formatter()
        self._reporter = get_reporter(context.connection.host_algorithm_manager, context.logger, context.input_provider)

    def _print(self, message):
        self._logger.info(message)

    def process(self, instruction: JobInstruction):
        manifest = self._context.manifest
        configuration = self._context.configuration

        reference = instruction.reference
        input_resources = manifest[Manifest.Key.INPUT]
        output_resources = manifest[Manifest.Key.OUTPUT]

        self._print(f"Starting with job: {reference}")
        self._print(f"With input: {input_resources}")
        self._print(f"Will output: {output_resources}")

        self._print("Putting sub-job-reference in environment variables..")
        os.environ["EP_ALGORITHM_SUB_JOB_REFERENCE"] = reference

        self._print("Clearing previous output..")
        clear_folder(self._context.configuration[Configuration.Key.OUTPUT_DIRECTORY])
        self._print("Cleared!")

        input_provider = self._context.input_provider

        self._print("Fetching all resources..")
        for resource in input_resources:

            resource_id = resource["name"]
            input_resources_context: dict = input_provider.get_input_resources_context()
            if resource_id not in input_resources_context:
                raise Exception(f"Expected {resource_id} in input resource context, but only has {input_resources_context.keys()}")
            
            resource_spec = input_resources_context[resource_id]
            resource_spec_patientcontext = resource_spec["patient-context"]
            resource_spec_patient_id = resource_spec_patientcontext["patient-id"]
            resource_spec_case_id = resource_spec_patientcontext["case-id"]
            resource_spec_resourcecontext = resource_spec["resource-context"]

            resource_instruction = {
                "store": resource["store"],
                "resource-identification": resource_id,
                "resource-filename": resource["data"],
                "resource-context": resource_spec_resourcecontext,
                "patient-context": {
                    "patient-id": resource_spec_patient_id,
                    "case-id": resource_spec_case_id
                }
            }

            self._print(f"Fetching resource {resource_instruction}..")

            fetched = self.resource_manager.fetch_resource(resource_instruction, self._context.configuration[Configuration.Key.INPUT_DIRECTORY])
            if not fetched:
                self._print(f"Could not fetch {resource}")
                self._publish_message(
                    self._message_formatter.get_message(reference, "failed", f"Could not download resource: {resource}"))
                return
            self._print("Fetched!")
        self._print("Fetched all!")

        self._print("Reading algorithm manifest..")
        command = manifest[Manifest.Key.COMMAND]
        
        self._print(f"Dispatching algorithm with command `{command}`..\n---------------\n")
        dispatch_command(command)
        self._print(f"\n---------------\nAlgorithm finished!")

        # TODO: Read report
        self._print("Reading algorithm execution report..")
        report = get_file_contents(configuration[Configuration.Key.OUTPUT_REPORT_LOCATION])
        self._print(f"Todo: process {report}")

        if report is None:
            status = "failed"
            description = "Algorithm failed!"
        else:
            status = "busy"
            description = "Algorithm finished! Writing back output.."
        
        self._print(description)

        # TODO: Send back data
        self._publish_message(
            self._message_formatter.get_message(reference, status, description))
        
        if status == "failed": return

        patient_id = input_provider.get_patient_id()
        case_id = input_provider.get_case_id()
        resource_context = f"job:{input_provider.get_reference()}"

        for resource in output_resources:
            resource_instruction = {
                "store": resource["store"],
                "resource-identification": resource["name"],
                "resource-filename": resource["data"],
                "resource-context": resource_context,
                "patient-context": {
                    "patient-id": patient_id,
                    "case-id": case_id
                }
            }
            self._print(f"Uploading resource {resource_instruction}..")

            posted = self.resource_manager.post_resource(resource_instruction, self._context.configuration[Configuration.Key.OUTPUT_DIRECTORY])

            if not posted:
                self._print("Could not post!! Failing")
                self._publish_message(
                    self._message_formatter.get_message(reference, "failed", "Could not upload result"))
                return

            self._print("Uploaded!")

        self._publish_message(
            self._message_formatter.get_message(reference, "finished", "Process completed"))
    
    def _publish_message(self, message: str):
        self._reporter.report(message)
        