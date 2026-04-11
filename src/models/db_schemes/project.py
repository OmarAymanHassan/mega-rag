from pydantic import BaseModel, Field, validator, field_validator
from typing import Optional
from bson.objectid import ObjectId



class Project(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    project_id: str = Field(..., min_length=1) # i want the min length is 1 --> can be 1 2 3 4 5 6 or 123 or 1231231231 but at min, the user should enter 1 value

    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True,
    }


    # what if the user enter !_)($) `special chars` inthe project_id ! --> i want to validate that!

    '''
    @validator("project_id")
    def validate_project_id(cls,value):
        if not value.isalnum():
            raise ValueError("Project id should be alphanumeric!!!")

        return value


    '''
    @field_validator("project_id")
    @classmethod
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError("Project id should be alphanumeric!!!")
        return value

    model_config = {
        "arbitrary_types_allowed": True
    }


    @classmethod
    def get_indexes(cls):

        return [

            {
                "key":[
                    ("project_id",1)
                ],
                "name": "project_id_index_1",
                "unique": True # every project_id should be unique, we dont want to have 2 projects with the same project_id


            }
        ]