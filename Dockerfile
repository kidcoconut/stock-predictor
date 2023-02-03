#--- local dev python is 3.10.8!
FROM python:3.8.16-slim-bullseye

# RUN apt-get -y update  && apt-get install -y \
#     python3-dev \
#     apt-utils \
#     python-dev \
#     build-essential \   
# && rm -rf /var/lib/apt/lists/* 

# RUN pip install --no-cache-dir -U pip
# RUN pip install --no-cache-dir -U cython
# RUN pip install --no-cache-dir -U numpy
# RUN pip install --no-cache-dir -U pystan

WORKDIR ./app
COPY docker_reqs.txt ./requirements.txt

RUN pip install --no-cache-dir -U -r  requirements.txt
COPY src/ .

EXPOSE 49300
CMD ["uvicorn", "main:app", "--workers=1", "--host=0.0.0.0", "--port=49300", "--reload"]


#---    Docker build log
#       from python:3.8; with fourthbrain reqs.txt          size:  1.6gb
#       from python:3.8; only prod_Reqs.txt                 size:  1.3gb
#       from python:3.10-slim-bullseye                      size:  520mb
#       from python:3.10-alpine                             size:  FAILED
#       from python:3.8.16-slim-bullseye                    size:  409mb
#       from python:3.8.16-slim-buster                      size:  520mb