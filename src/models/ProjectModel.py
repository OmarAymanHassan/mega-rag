from .BaseDataModel import BaseDataModel
from .enums.DataBaseEnums import DataBaseEnum
from .db_schemes import Project


class ProjectModel(BaseDataModel):

    def __init__(self, db_client):
        super().__init__(db_client)

        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]


    @classmethod
    async def create_instance(cls, db_client):
        instance = cls(db_client)
        await instance.init_collection()
        return instance
    

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]

            indexes = Project.get_indexes()

            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name = index["name"],
                    unique = index["unique"]
                )


    async def create_project(self, project:Project):

        # To use motor, i need to insert the data as dict, so i will use the model_dump() method to convert it to dict
        # insert_one() : to insert a single document into the collections
        result = await self.collection.insert_one(project.model_dump(by_alias=True, exclude_unset=True))
        project.id = result.inserted_id # to return the id of the inserted document
        return project
    


    async def get_project_or_create_one(self, project_id):


        record = await self.collection.find_one({
            "project_id": project_id
        })

        if record is None:
            project = Project(project_id=project_id)
            new_project = await self.create_project(project)
            return new_project
    
        return Project(**record) 
    

    async def get_all_projects(self, page:int = 1, page_size: int = 10):

        # get all documents inside our collection
        total_docs = await self.collection.count_documents({})

        # calc total of pages needed to carry all the documents

        total_pages = total_docs // page_size 
        if total_docs % page_size > 0:
            total_pages += 1

        
        # skip the documents of the previous pages and limit the result to the page size
        # find({}) dont filter based on anything, it will return all the documents, but we will use skip() and limit() to paginate the results
        cursor = self.collection.find({}).skip((page-1)*page_size).limit(page_size)


        projects = []
        async for document in cursor:
            projects.append(Project(**document)) # convert the document to a Project model and append it to the list of projects

        return projects, total_pages
    

