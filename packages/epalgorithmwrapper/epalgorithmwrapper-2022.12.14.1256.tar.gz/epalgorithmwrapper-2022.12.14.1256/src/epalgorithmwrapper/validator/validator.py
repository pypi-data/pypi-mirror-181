from ..utils.manifest import Manifest
from ..reporter.reporter import Reporter
from ..reporter.rest_api_reporter import RESTAPIReporter
from ..connection import get_algorithm_manager_host
import logging


def __valid_version(version_int: int):
    return version_int == 1

def __get_reporter() -> Reporter:
    host = get_algorithm_manager_host()
    logger = logging.getLogger(__name__)
    route = "algorithm-validated"
    return RESTAPIReporter(host, logger, route)

def get_in_out_message(in_or_out: list):
    return ",".join([
        f"""{{
            \"data-name\": \"{x["data"]}\",
            \"store\": \"filesystem\",
            \"name\": \"{x["name"]}\"
        }}""" for x in in_or_out])

def validate():
    manifest = Manifest.get_manifest()

    if Manifest.Key.MANIFEST_VERSION not in manifest:
        raise KeyError(f"Manifest version not present! Does have: {dict(manifest)}")
    
    manifest_version: str = manifest[Manifest.Key.MANIFEST_VERSION]  # v1
    manifest_version_int = int(manifest_version.replace("v", ""))    # 1
    manifest_version_valid = __valid_version(manifest_version_int)
    if not manifest_version_valid:
        raise KeyError("Manifest version is not supported")

    all_keys = Manifest.Key.COMMAND in manifest \
                and Manifest.Key.IDENTIFIER in manifest \
                and Manifest.Key.INPUT in manifest \
                and Manifest.Key.OUTPUT in manifest
    if not all_keys: return False

    command: str = manifest[Manifest.Key.COMMAND]
    identifier: str = manifest[Manifest.Key.IDENTIFIER]
    input: list = manifest[Manifest.Key.INPUT]
    output: list = manifest[Manifest.Key.OUTPUT]

    if type(input) is not list:
        raise KeyError("Manifest input should be a list of strings")
    if type(output) is not list:
        raise KeyError("Manifest output should be a list of strings")
    if type(command) is not str:
        raise KeyError("Manifest command should be a string")
    if type(identifier) is not dict:
        raise KeyError("Manifest identifier should be a dict")

    input_message = get_in_out_message(input)
    output_message = get_in_out_message(output)

    identifier_name = identifier["name"]
    identifier_version = identifier["version"]

    # TODO: Register to API that validation was successful, including name of algorithm, version, all taken from manifest
    reporter = __get_reporter()
    with reporter:
        message = f"""
        {{
            \"message-type\":\"algorithm-validated\",
            \"report\": {{
                \"status\": \"valid\"
            }},
            \"algorithm-description\":{{
                \"identifier\":{{
                    \"name\": \"{identifier_name}\",
                    \"version\": \"{identifier_version}\"
                }},
                \"input-resources\": [
                    {input_message}
                ],
                \"output-resources\": [
                    {output_message}
                ]
            }}
        }}
        """.strip()

        print("Sending validation message..")

        reporter.report(message)

        print("Validation message sent!")