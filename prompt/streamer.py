from typing import Union

from transformers import PreTrainedTokenizer, PreTrainedTokenizerFast
from huggingface_hub import InferenceClient

from prompt.messages import generate_message


def stream_messages(
    model_endpoint_url: str,
    huggingface_token: str,
    tokenizer: Union[PreTrainedTokenizer, PreTrainedTokenizerFast], 
    python_code: str
):
    messages = generate_message(python_code)
    text = tokenizer.apply_chat_template(
        conversation=messages,
        tokenize=False,
        add_generation_prompt=True
    )
    
    inference_client= InferenceClient(model=model_endpoint_url, token=huggingface_token) 
    stream = inference_client.text_generation(
        prompt=text,
        stream=True,
        details=False,
        max_new_tokens=2048
    )
    
    result = ""
    for r in stream:
        result += r
        yield result
    
    
    
    