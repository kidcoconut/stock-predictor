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
        curl --header "Content-Type: application/json" --request POST --data '{"ticker":"MSFT", "days":7}' http://0.0.0.0:49300/predict


# Quality Assurance:
    * conda activate wk12_prod
    * locally test: (python calls)
        * create a new model
        * run a prediction
    * docker test (repeat tast plan)
    * EC2 deploy and test (repeat test plan)


# Environment
- EC2 ssh connectivity
    - ssh -i "stock-pred-fastapi-mle10-wk12-imckone.pem" ec2-user@ec2-54-161-241-106.compute-1.amazonaws.com
    * Python:  v3.8.16
        * for Amazon EC2 hosting, to upgrade python, run:
            * sudo amazon-linux-extras install python3.8
            * sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

        * for adjusting symlinks
            * sudo rm /usr/bin/python  (which is only a link to /usr/bin/python2.7)
            * sudo ln -s /usr/bin/python3.8 /usr/bin/python

- Docker cmds
    - to build the image
        - docker build -t img-stock-prophet:qa .
    - to run the docker container
        - docker run -d --rm --name ctr-stock-prophet -p 49300:8000 img-stock-prophet:qa
    - to start an existing container
        - docker start -it ctr-stock-prophet /bin/bash 
        - docker exec -it ctr-stock-prophet /bin/bash


