from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from model import predict, convert


#--- fastAPI self doc descriptors
kstr_descr = """
    Fourthbrain Capstone:  MLE10 Cohort
    
    Stock Prophet 
    Getting an initial working system quickly into production

    data -> model -> API -> deployment (Amazon EC2)
    
    
    Deliverables:
    * Link to your public repository on GitHub
        * scripts model.py and main.py
        * requirements.txt (follow instructions for its creation)
        * README.md that includes how to cURL your API endpoint

    Objectives:
    * Develop a RESTful API with FastAPI
    * Build a basic time series model to predict stock prices
    * Deploy a FastAPI to AWS EC2
"""

tags_metadata = [
    {
        "name": "predict",
        "description": "Prophet stock predictions.",
    },
]
app = FastAPI(
    title="MLE10 Week12:  Iain McKone",
    description=kstr_descr,
    version="0.0.1",
    openapi_tags=tags_metadata
)

# pydantic models
class StockIn(BaseModel):
    ticker: str
    days: int

class StockOut(StockIn):
    forecast: dict


@app.get("/")
def get_index():
    return{"message:  stock predictor app - mle10"}

#--- endpoint for prediction api
@app.post("/predict", response_model=StockOut, status_code=200, tags=["predict"])
def get_prediction(payload: StockIn):
    ticker = payload.ticker
    days = payload.days

    prediction_list = predict(ticker, days)

    if not prediction_list:
        raise HTTPException(status_code=400, detail="Model not found.")

    response_object = {
        "ticker": ticker, 
        "days": days,
        "forecast": convert(prediction_list)}
    return response_object
