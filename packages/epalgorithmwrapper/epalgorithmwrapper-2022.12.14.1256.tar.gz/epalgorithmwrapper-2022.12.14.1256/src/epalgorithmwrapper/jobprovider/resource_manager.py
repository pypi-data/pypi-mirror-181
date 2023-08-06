from ..utils.context import Context
from ..utils.filesystem_utils import _fix_dirs

def get_resource_manager(context):
    return ResourceManager(context)

class ResourceManager:
    SUPPORTED_STORES = ["filesystem"]

    def __init__(self, context: Context):
        self._logger = context.logger
        self._repository_filesystem = RepositoryFileSystem(context)
        self._context = context

    def fetch_resource(self, resource_instruction, workdir):
        if resource_instruction is None:
            self._logger.warning("Fetching instruction was none!")
            return False

        store = resource_instruction["store"]
        self.__validate_store(store)
        
        if store == "filesystem":
            return self._repository_filesystem.fetch_resource(resource_instruction, workdir)
        return False
    
    def post_resource(self, resource_instruction, workdir):
        if resource_instruction is None:
            self._logger.warning("Posting instruction was none!")
            return False

        store = resource_instruction["store"]
        self.__validate_store(store)

        if store == "filesystem":
            return self._repository_filesystem.post_resource(resource_instruction, workdir)
    
    def __validate_store(self, store) -> bool:
        if store not in ResourceManager.SUPPORTED_STORES:
            raise NotImplementedError(f"Store {store} not supported")

    def _upload_resource_filesystem(self, workdir, filename):
        pass

class RepositoryFileSystem:
    def __init__(self, context: Context):
        self._logger = context.logger
        self.context = context

    def fetch_resource(self, resource_instruction, workdir):
        self._logger.info("Fetching data from filesystem..")

        data_provider = self.context.data_provider

        identification = resource_instruction["resource-identification"]
        patient_context = resource_instruction["patient-context"]
        patient_id = patient_context["patient-id"]
        case_id = patient_context["case-id"]
        filename = resource_instruction["resource-filename"]
        file_context = resource_instruction["resource-context"]

        request_body = {
            "patientId": patient_id,
            "caseId": case_id,
            "context": file_context,
            "fileName": filename
        }

        data = data_provider.send_request(request_body)
        if data is None: return False

        if data == True:
            self._logger.info("Data should be available")
            return True

        _fix_dirs(workdir)

        loc = f"{workdir}/{filename}"

        self._logger.info("Writing response..")
        with open(loc, 'wb+') as f:
            f.write(data)
        
        self._logger.info(f"Received {filename} from filesystem, saved into {loc}")
        return True
    
    def post_resource(self, resource_instruction, workdir):
        identification = resource_instruction["resource-identification"]
        patient_context = resource_instruction["patient-context"]
        patient_id = patient_context["patient-id"]
        case_id = patient_context["case-id"]
        filename = resource_instruction["resource-filename"]
        file_context = resource_instruction["resource-context"]

        data_uploader = self.context.data_uploader
        sent = data_uploader.send_request(
            patient_id=patient_id, 
            case_id=case_id, 
            file_context=file_context, 
            workdir=workdir, 
            filename=filename)

        return sent
