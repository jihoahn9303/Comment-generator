import threading
# import asyncio

from huggingface_hub import InferenceEndpoint, get_inference_endpoint, InferenceClient
from huggingface_hub._inference_endpoints import InferenceEndpointStatus


semaphore = threading.Semaphore(1)
# SEMAPHORE = asyncio.Semaphore(1)


def get_client(model_endpoint_url: str, huggingface_token: str) -> InferenceClient:
    return InferenceClient(
        model=model_endpoint_url,
        token=huggingface_token
    )

def get_endpoint(endpoint_name: str, namespace: str, huggingface_token: str) -> InferenceEndpoint:
    return get_inference_endpoint(
        name=endpoint_name,
        namespace=namespace,
        token=huggingface_token
    )

def get_endpoint_status(endpoint: InferenceEndpoint) -> InferenceEndpointStatus:
    '''
    PENDING = "pending"
    INITIALIZING = "initializing"
    UPDATING = "updating"
    UPDATE_FAILED = "updateFailed"
    RUNNING = "running"
    PAUSED = "paused"
    FAILED = "failed"
    SCALED_TO_ZERO = "scaledToZero"
    '''
    
    return endpoint.status

async def wait_for_endpoint(endpoint: InferenceEndpoint) -> InferenceEndpoint:
    try:
        status = get_endpoint_status(endpoint)
        if status in ['paused', 'scaledToZero', 'pending']:
            semaphore.acquire()
            endpoint.resume(running_ok=True)
            endpoint.fetch()
        endpoint.wait()
    finally:
        semaphore.release()
        return endpoint

