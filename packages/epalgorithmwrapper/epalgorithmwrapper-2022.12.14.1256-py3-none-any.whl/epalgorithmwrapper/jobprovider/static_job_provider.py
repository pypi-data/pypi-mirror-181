from ..utils.context import Context
from .message_processor import MessageProcessor
from .instruction import JobInstruction
from .job_provider import JobProvider

class StaticJobProvider(JobProvider):
    def __init__(self, 
            context: Context, 
            message_processor: MessageProcessor, 
            reference,
            patient_id:str,
            case_id:str):
        super().__init__()

        self._context = context
        self._message_processor = message_processor
        self._reference = reference
        self._patient_id = patient_id
        self._case_id = case_id

        self.init_job()

    def init_job(self):
        instruction = JobInstruction(self._reference, self._patient_id, self._case_id)
        self._message_processor.process(instruction)
    