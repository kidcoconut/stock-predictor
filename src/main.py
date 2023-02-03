from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from model import predict, convert
import joblib


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


#--- endpoint for training api

#--- endpoint for prediction api
@app.post("/predict", response_model=StockOut, status_code=200, tags=["predict"])
def get_prediction(payload: StockIn):
    ticker = payload.ticker
    days = payload.days

    #prediction_list = predict(ticker, days)
    prediction_list = predict(ticker, days)


    if not prediction_list:
        raise HTTPException(status_code=400, detail="Model not found.")

    response_object = {
        "ticker": ticker, 
        "days": days,
        "forecast": convert(prediction_list)}
    return response_object


def local_predict(ticker="MSFT", days=7):
    #--- CUSTOM: load from models folder
    pth_appRoot = Path(__file__).resolve().parent 

    pth_strAppRoot = str(pth_appRoot) + "/"
    pth_strModels =   pth_strAppRoot + "models/"
    pth_strPlots =   pth_strAppRoot + "plots/"

    model_file = pth_strModels + str(f"{ticker}.joblib")
    if not model_file.exists():
        return False

    TODAY = datetime.date.today()
    model = joblib.load(model_file)
    future = TODAY + datetime.timedelta(days=days)

    dates = pd.date_range(start="2020-01-01", end=future.strftime("%m/%d/%Y"),)
    df = pd.DataFrame({"ds": dates})

    forecast = model.predict(df)

    #--- CUSTOM: save to plots folder
    pthPlots = Path(BASE_DIR).joinpath("plots")
    pthPlots = pth_strPlots
    model.plot(forecast).savefig(pth_strPlots + str(f"{ticker}_plot.png"))
    model.plot_components(forecast).savefig(pth_strPlots + str(f"{ticker}_plot_components.png"))

    return forecast.tail(days).to_dict("records")