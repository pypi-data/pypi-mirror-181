"""
Flow360 base Model
"""
from datetime import datetime
from typing import List, Optional
from functools import wraps

from typing import Optional
from pydantic import BaseModel, Extra, Field

from flow360.cloud.http_util import RestApi


class Flow360BaseModel(BaseModel):
    """
    Flow360 base Model
    """

    name: str
    user_id: str = Field(alias="userId")
    solver_version: str = Field(alias="solverVersion")
    status: str
    tags: Optional[List[str]]
    created_at: Optional[str] = Field(alias="createdAt")
    updated_at: Optional[datetime] = Field(alias="updatedAt")
    updated_by: Optional[str] = Field(alias="updatedBy")

    class Config:
        extra=Extra.allow
        allow_mutation=False


def on_cloud_resource_only(func):
    @wraps(func)
    def wrapper(obj, *args, **kwargs):
        if not obj.is_cloud_resource():
            raise RuntimeError('Resource does not have "id", it is not a cloud resource. Provide "id" before calling this function.')
        return func(obj, *args, **kwargs)
    return wrapper


def before_submit_only(func):
    @wraps(func)
    def wrapper(obj, *args, **kwargs):
        if obj.is_cloud_resource():
            raise RuntimeError('Resource already have "id", cannot call this method. To modify and re-submit create a copy.')
        return func(obj, *args, **kwargs)
    return wrapper


class Flow360Resource(RestApi):
    def __init__(self, resource_type, INFO_TYPE_CLASS, S3_TRANSFER_METHOD=None, *args, **kwargs):
        self._resource_type = resource_type
        self.S3_TRANSFER_METHOD = S3_TRANSFER_METHOD
        self.INFO_TYPE_CLASS = INFO_TYPE_CLASS
        super().__init__(*args, **kwargs)

    def __str__(self):
        if self._info is not None:
            return self._info.__str__()
        else:
            return f'{self._resource_type} is not yet submitted.'

    def is_cloud_resource(self):
        return self.id is not None

    @on_cloud_resource_only
    def get_info(self, force=False):
        if self._info is None or force:
            self._info = self.INFO_TYPE_CLASS(**self.get())
        return self._info  

    @property
    def info(self):
        return self.get_info()    

    @property
    @on_cloud_resource_only
    def status(self):
        return self.get_info(True).status 

    @property
    def id(self):
        return self._id

    @property
    @on_cloud_resource_only
    def name(self):
        return self.info.name

    @property
    @on_cloud_resource_only
    def solver_version(self):
        return self.info.solver_version

    @on_cloud_resource_only
    def download(self, file_name, to_file=".", keep_folder: bool = True):
        self.S3_TRANSFER_METHOD.download_file(
            self.id, file_name, to_file, keep_folder
        )

    @on_cloud_resource_only
    def upload(self, remote_file_name: str, file_name: str):
        self.S3_TRANSFER_METHOD.upload_file(
            self.id, remote_file_name, file_name
        )


def is_object_cloud_resource(resource: Flow360Resource, msg=None):
    if resource is not None:
        if not resource.is_cloud_resource():
            raise RuntimeError('Reference resource is not a cloud resource. If a case was retried or forked from other case, submit the other case first before submitting this case.')
        return True    
    return False        