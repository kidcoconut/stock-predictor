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

# how to execute, test the app and endpoint
    * Run the app (locally):
        uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 49300
    
    * Test the endpoint (locally)
        curl \
        --header "Content-Type: application/json" \
        --request POST \
        --data '{"ticker":"MSFT", "days":7}' \
        http://0.0.0.0:49300/predict
