'''
    Here we define three functions (this model was developed by Andrew Clark):

    -   train() downloads historical stock data with yfinance, creates a new 
        Prophet model, fits the model to the stock data, and then serializes 
        and saves the model as a Joblib file.

    -   predict() loads and deserializes the saved model, generates a new 
        forecast, creates images of the forecast plot and forecast components, 
        and returns the days included in the forecast as a list of dicts.

    -   convert() takes the list of dicts from predict and outputs a dict of 
        dates and forecasted values; e.g., {"07/02/2020": 200}).

    The last block of code allows you to execute the model from the command 
    line, with two arguments, a valid stock ticker and the number of days to predict.
'''


import datetime
from pathlib import Path

import joblib
import pandas as pd
import yfinance as yf
from prophet import Prophet

import argparse

BASE_DIR = Path(__file__).resolve(strict=True).parent
TODAY = datetime.date.today()


def train(ticker="MSFT"):
    data = yf.download(ticker, "2020-01-01", TODAY.strftime("%Y-%m-%d"))

    df_forecast = data.copy()
    df_forecast.reset_index(inplace=True)
    df_forecast["ds"] = df_forecast["Date"]
    df_forecast["y"] = df_forecast["Adj Close"]
    df_forecast = df_forecast[["ds", "y"]]
    df_forecast

    #--- ERROR: ValueError: Column ds has timezone specified, which is not supported. Remove timezone.
    #df_forecast.drop(['timezone'], axis=1)
    #print("TRACE:  (train.df_forecast)", df_forecast.head().T)
    print("TRACE:  (train.df_forecast)", df_forecast.dtypes)

    #--- attempt to remove the timestamp attribute
    df_forecast['ds'] = df_forecast['ds'].dt.tz_localize(None)                      #--- did not work
    #df_forecast['ds'].apply(lambda x: x.replace(tzinfo=None))
    print("TRACE:  (train.df_forecast)", df_forecast.dtypes)

    model = Prophet()
    model.fit(df_forecast)

    joblib.dump(model, Path(BASE_DIR).joinpath(f"{ticker}.joblib"))


def predict(ticker="MSFT", days=7):
    model_file = Path(BASE_DIR).joinpath(f"{ticker}.joblib")
    if not model_file.exists():
        return False

    model = joblib.load(model_file)

    future = TODAY + datetime.timedelta(days=days)

    dates = pd.date_range(start="2020-01-01", end=future.strftime("%m/%d/%Y"),)
    df = pd.DataFrame({"ds": dates})

    forecast = model.predict(df)

    model.plot(forecast).savefig(f"{ticker}_plot.png")
    model.plot_components(forecast).savefig(f"{ticker}_plot_components.png")

    return forecast.tail(days).to_dict("records")

def convert(prediction_list):
    output = {}
    for data in prediction_list:
        date = data["ds"].strftime("%m/%d/%Y")
        output[date] = data["trend"]
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Predict')
    parser.add_argument('--ticker', type=str, default='MSFT', help='Stock Ticker')
    parser.add_argument('--days', type=int, default=7, help='Number of days to predict')
    args = parser.parse_args()
    
    train(args.ticker)
    prediction_list = predict(ticker=args.ticker, days=args.days)
    output = convert(prediction_list)
    print(output)