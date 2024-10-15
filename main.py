import os
from typing import Tuple

import gradio as gr
# from dotenv import load_dotenv
# load_dotenv()

from huggingface_hub import login, InferenceEndpoint
from huggingface_hub._inference_endpoints import InferenceEndpointStatus
from transformers import AutoTokenizer
from fastapi import FastAPI
from contextlib import asynccontextmanager

from prompt.streamer import stream_messages
from utils.huggingface_utils import get_endpoint, wait_for_endpoint

INFERENCE_INFOS = {
    'model_names': ['NTQAI/Nxcode-CQ-7B-orpo'],
    'tokenizer_paths': ['NTQAI/Nxcode-CQ-7B-orpo'],
    'tokenizers': [],
    'endpoint_names': [os.environ.get('NTQAI_ENDPOINT_NAME')],
    'hf_token': os.environ.get('HF_TOKEN'),
    'namespace': os.environ.get('HF_NAMESPACE')
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Login to HuggingFace hub
    token = INFERENCE_INFOS['hf_token']
    login(token=token, add_to_git_credential=True)
    
    # Load Tokenizer object from HuggingFace
    for tokenizer_path in INFERENCE_INFOS['tokenizer_paths']:
        INFERENCE_INFOS['tokenizers'].append(AutoTokenizer.from_pretrained(tokenizer_path))
        
    yield
    
    
app = FastAPI(lifespan=lifespan)


def check_endpoint_status(model_name: str) -> Tuple[InferenceEndpoint, InferenceEndpointStatus]:
    idx = INFERENCE_INFOS['model_names'].index(model_name)
    endpoint = get_endpoint(
        endpoint_name=INFERENCE_INFOS['endpoint_names'][idx],
        namespace=INFERENCE_INFOS['namespace'],
        huggingface_token=INFERENCE_INFOS['hf_token']
    )
    model_status = endpoint.status

    return endpoint, model_status


def is_model_ready(model_name: str) -> str:
    _, model_status = check_endpoint_status(model_name=model_name)
    
    if model_status == 'running':
        return "모델이 준비되었습니다. 멋진 코드를 만들어봐요!"
    else:
        return "아직 모델이 준비되지 않았습니다. 모델을 불러오기 버튼을 눌러주세요!"
    
    
async def load_pretrained_model(model_name: str) -> str:
    endpoint, endpoint_status = check_endpoint_status(model_name)
    
    if endpoint_status in ['paused', 'scaledToZero']:
        await wait_for_endpoint(endpoint)
        
    return "모델이 준비되었습니다. 멋진 코드를 만들어봐요!"

    
def generate_comments(python_code: str, model_name: str):
    try:
        endpoint, endpoint_status = check_endpoint_status(model_name)
        if endpoint_status == 'running':
            idx = INFERENCE_INFOS['model_names'].index(model_name)
            result = stream_messages(
                model_endpoint_url=endpoint.url,
                huggingface_token=INFERENCE_INFOS['hf_token'],
                tokenizer=INFERENCE_INFOS['tokenizers'][idx], 
                python_code=python_code
            )
            for stream_so_far in result:
                yield stream_so_far 
        else:
            yield "아직 모델이 준비되지 않았습니다. 모델을 불러오기 버튼을 눌러주세요!"
    except ValueError:
        print(f"Unknown model: {model_name}")
        


@app.get("/main")
async def main():
    return {"message": "FastAPI 애플리케이션이 정상적으로 동작 중입니다!"}
    
    
def create_gradio_ui() -> gr.Blocks:
    with gr.Blocks() as ui:
        gr.Markdown("### 자동으로 Python 코드 주석을 추가해줍니다😏 ###")
        with gr.Row():
            model_status = gr.Textbox(
                label="모델 준비 상태를 보여줍니다✌",
                lines=1,
                max_lines=1,
                interactive=False
            )
        with gr.Row():
            input_python_code = gr.Textbox(
                label="파이썬 코드를 입력해주세요! 최대 문자 길이는 2048자입니다.",
                lines=10,
                max_length=2048
            )
            output_python_code = gr.Textbox(
                label='''
                주석이 추가되었습니다!
                여러분들이 작성한 멋진 코드를 남들에게 자랑해주세요😊
                ''',
                lines=10,
            )
        with gr.Row():
            model = gr.Dropdown(
                choices=["NTQAI/Nxcode-CQ-7B-orpo"], 
                label="모델을 선택해주세요✌", 
                value="NTQAI/Nxcode-CQ-7B-orpo"
            )
        with gr.Row():
            model_ready = gr.Button("모델 상태 확인")
            comment_adder = gr.Button("주석 추가")
            clear = gr.Button("Clear textbox")
        with gr.Row():
            load_model = gr.Button("모델 불러오기🦾")
            
        def clear_texts():
            return "", ""
        
        model_ready.click(
            fn=is_model_ready,
            inputs=[model],
            outputs=[model_status]
        )
        comment_adder.click(
            fn=generate_comments,
            inputs=[input_python_code, model],
            outputs=[output_python_code],
            concurrency_limit=10,
            queue=True
        )
        clear.click(
            fn=clear_texts,
            outputs=[input_python_code, output_python_code]
        )
        load_model.click(
            fn=load_pretrained_model,
            inputs=[model],
            outputs=[model_status],
            concurrency_limit=5   
        )
        
        return ui
    
    
ui = create_gradio_ui()
app = gr.mount_gradio_app(app, ui, path="/gradio")






