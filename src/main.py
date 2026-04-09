from fastapi import FastAPI
#load_dotenv() # we pass it as i, since the default value is `.env` if it has different name we pass it load_dotenv(".new_name")

from routes import base,data

app = FastAPI()

app.include_router(base.base_router)
app.include_router(data.data_router)



# we will run this on port 5000 and make anyone outside the network can access it !
## uvicorn main:app --reload --host 0.0.0.0 --port 5000

