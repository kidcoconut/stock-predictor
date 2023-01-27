from fastapi import FastAPI
app = FastAPI()

@app.get("/ping")
def pong():
    return {"ping": "pong!"}



'''
uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 49300
'''