# stock-predictor
a RESTful API with FastAPI and basic time series model to predict stock prices


# Deliverables:
    * Link to public repository on GitHub
    * scripts model.py and main.py
    * requirements.txt (follow instructions for its creation)
    * README.md that includes how to cURL your API endpoint


# Learning Objectives
By the end of this lesson, you will be able to:
    * Develop a RESTful API with FastAPI
    * Build a basic time series model to predict stock prices
    * Deploy a FastAPI to AWS EC2


# HOW TO:  create a new model
    python model.py --ticker <yahoo ticker> --days <num days>
        eg. python model.py --ticker AAPL --days 7


# HOW TO:  run a prediction
    * Run the app (locally):
        uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 49300
    
    * Test the endpoint (locally)
        curl \
        --header "Content-Type: application/json" \
        --request POST \
        --data '{"ticker":"MSFT", "days":7}' \
        http://0.0.0.0:49300/predict
