from enum import Enum


class ResponseSignal(Enum):


    FILE_VALIDATED_SUCESFULLY = "file_validated_sucessfully"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOADED_SUCESSFULLY = "file_uploaded_sucessfully"
    FILE_UPLOADED_FAILURE = "file_uploaded_failure"
    FILE_NOT_FOUND = "No file was uploaded"

