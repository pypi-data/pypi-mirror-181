import os

EP_ENVIRONMENT_KEY = "EP_ENVIRONMENT"

DEFAULT_HOST = "localhost"
DOCKER_HOST = "rabbitmq"
DEFAULT_FILESYSTEM_HOST = "localhost:5101"
DOCKER_FILESYSTEM_HOST = "repository-filesystem:5101"
DEFAULT_ALGORITHMMANAGER_HOST = "localhost:5002"
DOCKER_ALGORITHMMANAGER_HOST = "algorithm-manager:5002"
DEFAULT_REGISTRY_HOST = "localhost:5080"
DOCKER_REGISTRY_HOST = "registry:5080"

def get_messagebroker_host():
    host = DEFAULT_HOST
    if EP_ENVIRONMENT_KEY not in os.environ:
        return host

    environment = os.environ[EP_ENVIRONMENT_KEY]
    if environment.find("_DOCKER") != -1:
        host = DOCKER_HOST
    
    return host

def get_filesystem_host():
    host = DEFAULT_FILESYSTEM_HOST
    if EP_ENVIRONMENT_KEY not in os.environ:
        return host

    environment = os.environ[EP_ENVIRONMENT_KEY]
    if environment.find("_DOCKER") != -1:
        host = DOCKER_FILESYSTEM_HOST
    
    return host

def get_algorithm_manager_host():
    host = DEFAULT_ALGORITHMMANAGER_HOST
    if EP_ENVIRONMENT_KEY not in os.environ:
        return host

    environment = os.environ[EP_ENVIRONMENT_KEY]
    if environment.find("_DOCKER") != -1:
        host = DOCKER_ALGORITHMMANAGER_HOST
    
    return host

def get_registry_host():
    host = DEFAULT_REGISTRY_HOST
    if EP_ENVIRONMENT_KEY not in os.environ:
        return host

    environment = os.environ[EP_ENVIRONMENT_KEY]
    if environment.find("_DOCKER") != -1:
        host = DOCKER_REGISTRY_HOST
    
    return host

def get_creds_provider():
    return lambda: ("admin", "admin")