from fastapi import FastAPI, APIRouter,Depends,UploadFile, status
from fastapi.responses import JSONResponse
from utils.config import get_settings,Settings
from controllers import DataController, ProjectController
from models import ResponseSignal
import aiofiles
import logging
import os


#logger = logging.getLogger(__name__)
logger = logging.getLogger("uvicorn-error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1" , "data"]
)


@data_router.post("/upload/{project_id}")
async def upload_data(project_id,
                      file:UploadFile,
                      app_settings:Settings = Depends(get_settings)
                      ):
    
    data_controller = DataController()

    is_valid, message_signal = data_controller.validated_uploaded_file(file)
    print(message_signal.value)


    if not is_valid:

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": is_valid,
                "result" : message_signal.value # to return enum_value
            }
        )

    

    file_path, file_id= data_controller.generate_unique_filepath(file.filename, project_id) # name of the file inside project_dir_path

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error while uploading the file: {e}")

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": ResponseSignal.FILE_UPLOADED_FAILURE.value,
            }
        )



    return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_UPLOADED_SUCESSFULLY.value,
            "file_id": file_id # return the unique filename to be stored in db
        }
    )