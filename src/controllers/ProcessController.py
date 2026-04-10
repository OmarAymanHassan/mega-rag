from .BaseController import BaseController
from .ProjectController import ProjectController
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from models import ProcessingEnum
from routes.schemes.data import ProcessRequest


import os


class ProcessController(BaseController):

    def __init__(self,project_id):
        super().__init__()

        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id) # src/assets/file/{project_id}/


    
    def get_file_extension(self,file_id):

        return os.path.splitext(file_id)[-1].lower() # get the extension like .txt or .pdf
    

    def get_file_loader(self, file_id):

        file_extension = self.get_file_extension(file_id)
        file_path = os.path.join(self.project_path, file_id) #src/assets/file/{project_id}/file_name.pdf or .txt


        if file_extension == ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding="utf-8")


        if file_extension == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)

        return None
    


    def get_file_content(self, file_id):
        
        loader = self.get_file_loader(file_id) # loader contains two main parts: page_content and metadata
        # page_content which contains the file text
        # metadata contains information about the file, like how many pages this file contains, extension, source ..etc.
        return loader.load()


    # i will use Recursive Charachter Text splitter instead of Charachter text-splitter
    # - since recursive, be more aware of context, dont cut in mid of sentece, be aware of newlines 
    # so it cuts in the beginning of newlines or endline and try as best as possible not to cut in middle of sentence



    def process_file_content(self, file_content:list, chunk_size:int = 100, overlap_size:int=20):

        #loader = self.get_file_content(file_id)

        file_chunks = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap_size, length_function = len)

        # extract the page content

        file_content_splis= [
            rec.page_content
            for rec in file_content
        ]

        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]

        chunks = file_chunks.create_documents(texts=file_content_splis, metadatas=file_content_metadata)
        #texts = file_chunks.create_documents(loader)

        return chunks