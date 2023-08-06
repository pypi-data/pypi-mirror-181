import json
from eputils.thread.consumer import ConsumerThread
from ..utils.context import Context
from .message_processor import MessageProcessor
from .instruction import JobInstruction
from .job_provider import JobProvider

class RabbitMQJobProvider(JobProvider):
    def __init__(self, context: Context, message_processor: MessageProcessor):
        super().__init__()

        self._jobs = {}
        self._message_processor = message_processor
        self._logger = context.logger
        self._context = context

        self._fetcher = RabbitMQBasicConsumer(context.connection.host, 
                                              context.connection.creds_provider,
                                              context.messagebus.job_queue_name, 
                                              self._on_receive, 
                                              context).run()
    
    def get_job(self, id):
        return self._jobs[id]

    def _validate(self, data):
        if "message-type" not in data: 
            raise NotImplementedError("Cannot interpret message: No message type")
        if not data["message-type"] == "algorithm": 
            raise NotImplementedError("Cannot interpret message: Unknown message type")

    def _on_receive(self, data):
        json_data = json.loads(data)
        self._validate(json_data)

        input_resources: list = json_data["input-resources"]
        output_resources: list = json_data["output-resources"]
        sub_job_reference: str = json_data["sub-job-reference"]
        
        instruction = JobInstruction(sub_job_reference, input_resources, output_resources)

        self._message_processor.process(instruction)

class RabbitMQBasicConsumer:
    def __init__(self, host, creds_provider, queue_name, on_receive, context: Context):
        self._host = host
        self._creds_provider = creds_provider
        self._on_receive = on_receive
        self._queue_name = queue_name
        self._logger = context.logger
        self._context = context

    def run(self):
        '''
        Start polling action for fetching jobs
        '''
        self._thread = ConsumerThread(host=self._host, 
                                      queue_name=self._queue_name, 
                                      creds_provider=self._context.connection.creds_provider, 
                                      on_receive=self._on_receive, 
                                      app_id=f"{self._context.messagebus.app_id}.job-provider",
                                      logger=self._logger)
        self._context.add_thread(self._thread)
        
        self._logger.info("Starting RabbitMQ Consumer thread..")
        self._logger.info(f"Listening to queue {self._queue_name}..")
        self._thread.start()

        return self
