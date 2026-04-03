from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def hello_world():
    return "Welcome to FastAPI - New version"

@app.get("/welcome")
def welcome():
    return {
        "message" : "Welcome to our website"
    }


# we will run this on port 5000 and make anyone outside the network can access it !
## uvicorn main:app --reload --host 0.0.0.0 --port 5000

