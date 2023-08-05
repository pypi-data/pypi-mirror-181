"""
API Contracts for DW Operation Sets
"""
from datetime import datetime
from typing import List, Optional, Any

from pydantic import BaseModel, Field

from pyrasgo.schemas import dataset as datasets_contracts
from pyrasgo.schemas import dw_operation as op_contracts
from pyrasgo.schemas import jobs as job_contracts


class OperationSetCreate(BaseModel):
    """
    Contract to create an operation set
    """

    name: Optional[str]
    operations: Optional[List[op_contracts.OperationCreate]]
    dataset_dependency_ids: Optional[List[int]] = Field(alias="datasetDependencyIds")  # Dataset Ids
    use_custom_sql: Optional[bool] = Field(alias='useCustomSql')
    sql: Optional[str]
    terminal_operation_resource_key: Optional[str] = Field(alias="terminalOperationResourceKey")
    description: Optional[str]
    attributes: Optional[dict]
    tags: Optional[List[str]]

    class Config:
        allow_population_by_field_name = True


class OperationSetUpdate(BaseModel):
    """
    Contract to update an operation set
    """

    name: Optional[str]
    operations: Optional[List[op_contracts.OperationUpdate]]
    dataset_dependency_ids: Optional[List[int]] = Field(alias="datasetDependencyIds")  # Dataset Ids
    use_custom_sql: Optional[bool] = Field(alias='useCustomSql')
    sql: Optional[str]
    terminal_operation_resource_key: Optional[str] = Field(alias="terminalOperationResourceKey")
    description: Optional[str]
    attributes: Optional[dict]
    tags: Optional[List[str]]

    class Config:
        allow_population_by_field_name = True


class OperationSet(BaseModel):
    """
    Contract to return from get endpoints
    """

    id: Optional[int]
    name: Optional[str]
    resource_key: Optional[str] = Field(alias='resourceKey')
    description: Optional[str]
    attributes: Optional[dict]
    tags: Optional[List[str]]
    operations: Optional[List[op_contracts.Operation]]
    dataset_dependencies: Optional[List[datasets_contracts.Dataset]] = Field(alias="datasetDependencies")
    fqtn_dependencies: Optional[List[str]] = Field(alias="fqtnDependencies")
    use_custom_sql: Optional[bool] = Field(alias='useCustomSql')
    sql: Optional[str]
    terminal_operation_resource_key: Optional[str] = Field(alias="terminalOperationResourceKey")
    organization_id: Optional[int] = Field(alias="organizationId")
    async_tasks: Optional[List[job_contracts.AsyncUpdateTask]] = Field(alias="asyncTasks")
    is_published: Optional[bool] = Field(alias="isPublished")

    class Config:
        allow_population_by_field_name = True


class NestedDataset(BaseModel):
    """
    Contract to safely nest in an OperationSet response
    """

    id: Optional[int]
    resource_key: Optional[str] = Field(alias="resourceKey")
    fqtn: Optional[str]

    class Config:
        allow_population_by_field_name = True


class BulkOperationSet(BaseModel):
    """
    Contract to return from get endpoints
    """

    id: Optional[int]
    resource_key: Optional[str] = Field(alias="resourceKey")
    name: Optional[str]
    organization_id: Optional[int] = Field(alias="organizationId")
    description: Optional[str]
    attributes: Optional[dict]
    tags: Optional[List[str]]
    use_custom_sql: Optional[bool] = Field(alias='useCustomSql')
    sql: Optional[str]
    is_published: Optional[bool] = Field(alias="isPublished")
    dataset: Optional[NestedDataset]
    dataset_dependencies: Optional[List[int]] = Field(alias="datasetDependencies")
    create_timestamp: Optional[datetime] = Field(alias="createTimestamp")
    create_author: Optional[int] = Field(alias="createdBy")
    create_author_full_name: Optional[str] = Field(alias="createAuthorFullName")
    update_timestamp: Optional[datetime] = Field(alias="updateTimestamp")
    update_author: Optional[int] = Field(alias="updatedBy")

    class Config:
        allow_population_by_field_name = True


class OperationSetAsyncEvent(BaseModel):
    """
    Represents a single event that happened while executing an async OperationSetCreate task
    """

    id: int
    create_timestamp: datetime = Field(alias='createTimestamp')
    event_type: str = Field(alias='eventType')
    message: Optional[Any]


class OperationSetAsyncTask(BaseModel):
    """
    Response model for when a caller asks to create a task or polls for that task's status
    """

    id: int = Field()
    request: OperationSetCreate = Field()
    create_author: Optional[int] = Field(alias='createAuthor')
    organization_id: int = Field(alias='organizationId')
    events: List[OperationSetAsyncEvent]
