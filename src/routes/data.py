from fastapi import FastAPI, APIRouter,Depends,UploadFile, status, Request
from fastapi.responses import JSONResponse
from utils.config import get_settings,Settings
from controllers import DataController, ProjectController,ProcessController
from models import ResponseSignal
from .schemes.data import ProcessRequest
from models.ProjectModel import ProjectModel
from models.db_schemes import DataChunk
from models.ChunkModel import ChunkModel
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
async def upload_data(request:Request,
                        project_id:str,
                      file:UploadFile,
                      app_settings:Settings = Depends(get_settings)
                      ):
    

    project_model = await ProjectModel.create_instance(db_client= request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id)
    
    data_controller = DataController()

    is_valid, message_signal = data_controller.validated_uploaded_file(file)
    print(message_signal.value)


    if not is_valid:

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": is_valid,
                "result" : message_signal.value, # to return enum_value
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




# ---------------------------------- Request Processing Endpoint ---------------------------------- #

@data_router.post("/process/{project_id}")
async def process_endpoint(project_id, process_request:ProcessRequest, request:Request):

    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset

    # get db connection

    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id)

  


    # init our process controller to use all its functionalities
    process_controller = ProcessController(project_id)

    # get the content of the file

    file_content = process_controller.get_file_content(file_id)
    file_chunks = process_controller.process_file_content(file_content=file_content, chunk_size=chunk_size, overlap_size=overlap_size)

    serialized_chunks = [
        {
            "page_content": chunk.page_content,
            "metadata": chunk.metadata
        }
        for chunk in file_chunks
    ]

    if not serialized_chunks or len(serialized_chunks)==0:
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={

                "signal":ResponseSignal.PROCESSING_FAILED.value

            }
        )


    # if there is serialized_chunks
    
    file_chunks_record = [
        DataChunk(
            chunk_text= chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order= i+1,
            chunk_project_id=project.id
        )


         for i, chunk in enumerate(file_chunks)
    ]

    chunk_model = await ChunkModel.create_instance(request.app.db_client)

    if do_reset ==1:
        _ = await chunk_model.delete_chunks_by_project_it(project_id= project.id)
        # delete all chunks of that project_id

    # add the new chunks
    num_records = await chunk_model.insert_many_chunks(chunks=file_chunks_record, batch_size=20)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "signal": ResponseSignal.PROCESSING_SUCESS.value,
            "inserted_chunks": num_records
        }
    )