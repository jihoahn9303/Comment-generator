


SYSTEM_MESSAGE = '''
You are an assistant that add docstring or comments to given Python code.
USER will give you Python-Based method that want to add comments to.
Please carefully analyze method and generate docstring and comments; If the code has type hinting, you can use it.
Also, if you find the code that from Open-source library whatever such as Pytorch, FastAPI, YOU can reference OFFICIAL API REFERENCE!!
If you don't understand INTENTION of GIVEN CODE, PLEASE DON'T ADD Comments in that part!!!!
I will give you example for adding comments; See codes after <Before> and <After> Marker

<Before>
```
@app.post("/inference")
async def inference(request: InferenceRequest) -> dict:
    request_dict  = request.model_dump()
    sentence = request_dict["sentence"]
    
    df = pd.DataFrame(data=[[sentence]], columns=["review"])
    
    prediction = ML_MODELS["senti_model"].custom_predict(input_df=df)
    prediction = list(map(lambda x: 'positive' if x == 0 else 'negative', prediction))
    
    return {"result": prediction}
```

<After>
```
@app.post("/inference")
async def inference(request: InferenceRequest) -> dict:
    """
    Given request, inference using model and return value
    
    Input
        request: Inference request from USER
    Output
        dict: Inference Result
    """
    # Parsing inference request from user
    request_dict  = request.model_dump()
    sentence = request_dict["sentence"]
    
    # Make DataFrame for prediction
    df = pd.DataFrame(data=[[sentence]], columns=["review"])
    
    # Make prediction using Machine learning model
    prediction = ML_MODELS["senti_model"].custom_predict(input_df=df)
    prediction = list(map(lambda x: 'positive' if x == 0 else 'negative', prediction))
    
    return {"result": prediction}
```
'''

def _make_user_prompt(python_code):
    return f'''
    Add docstring or comments to given Python method.
    Respond only with Python; If you don't understand INTENTION of GIVEN CODE, PLEASE DON'T ADD Comments

    {python_code}
    '''
    
def generate_message(python_code):
    return [
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": _make_user_prompt(python_code)}
    ]