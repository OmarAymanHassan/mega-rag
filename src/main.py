from fastapi import FastAPI
#load_dotenv() # we pass it as i, since the default value is `.env` if it has different name we pass it load_dotenv(".new_name")
from motor.motor_asyncio import AsyncIOMotorClient
from utils.config import get_settings

from contextlib import asynccontextmanager

from routes import base,data


'''
@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL) # connect to the url of mongodb
    app.db_client = app.mongo_conn[settings.MONGODBDB_DATABASE]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()
'''

@asynccontextmanager
async def db_connection(app:FastAPI):
    settings = get_settings()

    #Startup the mongodb
    print("Starting the mongodb server...")
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODBDB_DATABASE]

    yield

    #closing mongodb
    print("Closing Mongodb ...")
    app.mongo_conn.close()

app = FastAPI(lifespan=db_connection)


app.include_router(base.base_router)
app.include_router(data.data_router)



# we will run this on port 5000 and make anyone outside the network can access it !
## uvicorn main:app --reload --host 0.0.0.0 --port 5000

