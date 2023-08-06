from .rabbitmq_job_provider import RabbitMQJobProvider
from .static_job_provider import StaticJobProvider
from ..utils.input_provider import InputProvider

def get_job_provider(input_provider: InputProvider, context, message_processor):
    input_type = input_provider.get_input_type()
    if input_type == "environment" or input_type == "cli":
        return StaticJobProvider(
            context, 
            message_processor, 
            input_provider.get_reference(),
            input_provider.get_patient_id(),
            input_provider.get_case_id())
    elif input_type == "rabbitmq":
        return RabbitMQJobProvider(
            context, 
            message_processor)