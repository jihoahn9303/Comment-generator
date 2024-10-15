# Comment Generator with Gradio + FastAPI

**수많은 주석을 일일이 타이핑하기 싫은 당신을 위한 프로젝트입니다😏**

Gradio UI에 코드를 입력하면, 자동으로 주석을 추가해주는 애플리케이션을 제작하였습니다 :)



## Project process

![Comment_generator excalidraw](https://github.com/user-attachments/assets/4f1fc567-10cd-47d5-83ae-acb09106babf)

1. 개발 환경에서 `Makefile`을 이용하여 `FastAPI` 기반 어플리케이션을 `Docker image`로 `build`합니다.

2. `Makefile`에 명시된 파이프라인에 따라, 빌드가 끝난 `Docker image`는 `GCP Artifact Registry`에 자동으로 배포됩니다.

3. `Makefile`에 명시된 파이프라인에 따라, `GCP VM Instance`를 자동으로 생성합니다.

4. 생성된 `VM Instance`는 자동으로 `GCP Artifact Registry`에서 `Docker image`를 가져오고, 컨테이너를 실행합니다 > `FastAPI 어플리케이션 실행`

5. 이제, 여러분들은 `Gradio UI`를 통해 자동으로 코드 주석을 만들 수 있습니다 :)



## Usage

### 서비스 URL

브라우저를 통해, Gradio UI에 접근할 수 있습니다. 주소는 아래와 같아요!

```
http://34.22.74.209:8000/gradio/
```

### Gradio UI

Gradio UI는 아래 그림과 같아요! 

![초기화면](https://github.com/user-attachments/assets/fa4a7a55-aee3-4cb7-8619-060e6e92a46c)

크게 다음과 같은 컴포넌트로 구성되어 있습니다.

```
1. 모델 준비 상태 확인 -> 코드 주석 생성을 위해 필요한 LLM 모델이 준비됐는지 확인합니다.
2. 파이썬 코드 입력 파트 -> 원본 파이썬 코드를 입력하는 곳입니다.
3. 주석 디스플레이 -> LLM 모델에 의해 추가된 주석을 보여주는 곳입니다.
4. 모델 선택 -> 코드 주석 생성에 사용할 LLM 모델을 선택할 수 있습니다.
```

모델이 준비되지 않은 경우에는, 주석을 생성할 수 없습니다. 이때, `모델 불러오기` 버튼을 클릭하여 모델을 로딩해주세요 (약 5~6분 소요)

```
<참고 사항>
- 비용 절감 차원으로, HuggingFace에서 제공하는 Dedicated endpoint 기능을 활용하였습니다.
- 해당 Endpoint를 호출할 시, 지정한 오픈 소스 LLM 모델을 사용하여 주석 생성을 수행합니다.
- 만약, 특정 시간(15분) 동안 Endpoint 호출이 없을 경우, Endpoint는 자동으로 중지됩니다.
- 모델 불러오기 버튼을 통해, Endpoint를 다시 활성화하는 과정을 수행합니다.
```


## Develop & Experiment environment

개발 환경에 대한 주요 사항은 아래와 같습니다.

| Source                  | Version                                                                               |
| ----------------------- | ------------------------------------------------------------------------------------- |
| OS(Host)                | Host: Microsoft Windows 10 Pro build `19045` / NVIDIA GeForce RTX 3060 12GB           |
| Remote controller       | WSL2 / Ubuntu version: `20.04`                                                        |
| Python                  | `3.11.10`                                                                             |
| IDLE                    | Visual Studio code `1.75.1`                                                           |
| Docker                  | Docker desktop `4.26.1` / Engine version: `24.0.7`                                    |


## To-do list

1. Gradio 커스텀 UI 개선 작업(가시성 측면)

2. 사용 가능한 LLM 모델 추가

3. 프로젝트 코드 주석 추가