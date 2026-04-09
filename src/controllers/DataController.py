from .BaseController import BaseController
from .ProjectController import  ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import re
import os


class DataController(BaseController):

    def __init__(self):
        # now the app_settings from basecontroller is called
        super().__init__()

        # to convert from megabyte to bytes
        self.size_scale = 1048576


    def validated_uploaded_file(self,file:UploadFile):
       
       # if there is no file uploaded
       if file is None or not file.filename:
           return False, ResponseSignal.FILE_NOT_FOUND
       
       if file.content_type  not in self.app_settings.FILE_ALLOWED_TYPES:
          
          return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED
       

       # file.size return size in bytes but FILE_MAX_SIZE is in MB

       if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
           return False, ResponseSignal.FILE_SIZE_EXCEEDED

       return True, ResponseSignal.FILE_UPLOADED_SUCESSFULLY



    def generate_unique_filepath(self, original_filename, project_id):

        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id)

        cleaned_filename = self.get_clean_filename(original_filename)

        new_file_path = os.path.join(project_path, random_key + "_" + cleaned_filename) # create a completely unique filename

           
        # loop on the file, if there is one with that name --> generate new_random_key and append it to the file

        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path =  new_file_path = os.path.join(project_path, random_key + "_" + cleaned_filename)


        return new_file_path, random_key + "_" + cleaned_filename # return the unique file path and the unique filename to be stored
    
    

    
    def get_clean_filename(self, original_filename):


        # remove any special charachter, except _ and .

        cleaned_filename = re.sub(r'[^\w.]', "" , original_filename.strip())

        # replace space with underscore
        cleaned_filename = cleaned_filename.replace(" ", "_")

        return cleaned_filename



