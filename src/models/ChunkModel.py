from .BaseDataModel import BaseDataModel
from .enums.DataBaseEnums import DataBaseEnum
from .db_schemes import DataChunk
from bson.objectid import ObjectId
from pymongo import InsertOne


class ChunkModel(BaseDataModel):

    def __init__(self, db_client):
        super().__init__(db_client)
        self.collections = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]

    
    @classmethod
    async def create_instance(cls, db_client):
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_CHUNK_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]

            indexes = DataChunk.get_indexes()

            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name = index["name"],
                    unique = index["unique"]
                )
    async def create_chunk(self, chunk:DataChunk):

        result = await self.collections.insert_one(chunk.model_dump(by_alias=True, exclude_unset=True))
        chunk.id = result.inserted_id # to return the id of the inserted document

        return chunk
    

    async def get_chunk_by_id(self, chunk_id:str):

        record = await self.collections.find_one({
            "id": ObjectId(chunk_id)
        })

        if not record:
            return None
        
        return DataChunk(**record)
    


    async def insert_many_chunks(self, chunks:list, batch_size:int = 100):

        for i in range(0,len(chunks), batch_size):
            batch = chunks[i : i+batch_size]

            operations=[
                InsertOne(chunk.model_dump(by_alias = True, exclude_unset = True))
                for chunk in batch
            ]

            await self.collections.bulk_write(operations)


        return len(chunks)
    


    async def delete_chunks_by_project_it(self, project_id:ObjectId):

        result = await self.collections.delete_many({
            "chunk_project_id": project_id
        })

        return result.deleted_count
    
