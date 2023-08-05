from datetime import datetime
from typing import List, Optional, Dict

from pydantic import BaseModel, Field

from pyrasgo.schemas import dataset_column as dataset_column_schemas
from pyrasgo.schemas import dw_table as dw_table_schemas
from pyrasgo.schemas import user as user_schemas


class Dataset(BaseModel):
    """
    Contract to return from get by id endpoints
    """

    id: int
    name: str
    resource_key: str = Field(alias='resourceKey')
    description: Optional[str]
    is_source: Optional[bool] = Field(alias='isSource')

    organization_id: Optional[int] = Field(alias='organizationId')
    dw_table_id: Optional[int] = Field(alias='dwTableId')
    dw_operation_set_id: Optional[int] = Field(alias='dwOperationSetId')

    columns: Optional[List[dataset_column_schemas.DatasetColumn]]
    dw_table: Optional[dw_table_schemas.DataTableWithColumns] = Field(alias='dataTable')
    fqtn: Optional[str]
    table_type: Optional[str] = Field(alias="tableType")
    consumer_count: int = Field(alias='consumerCount')

    attributes: Optional[Dict[str, str]]
    tags: Optional[List[str]]
    owners: Optional[List[user_schemas.NestedUser]]

    create_timestamp: Optional[datetime] = Field(alias='createTimestamp')
    create_author: Optional[int] = Field(alias='createdBy')
    update_timestamp: Optional[datetime] = Field(alias='updateTimestamp')
    update_author: Optional[int] = Field(alias='updatedBy')
    source_type: Optional[str] = Field(alias='sourceType', default="RASGO")

    verified_user: Optional[user_schemas.NestedUser] = Field(alias="verifiedUser")
    verified_timestamp: Optional[datetime] = Field(alias="verifiedTimestamp")

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


class DatasetBulk(BaseModel):
    """
    Contract to return from get list endpoints
    """

    id: int
    name: str
    resource_key: str = Field(alias='resourceKey')
    description: Optional[str]
    is_source: Optional[bool] = Field(alias='isSource')

    organization_id: Optional[int] = Field(alias='organizationId')

    dw_table_id: Optional[int] = Field(alias='dwTableId')
    dw_table: Optional[dw_table_schemas.DataTable] = Field(alias='dataTable')
    fqtn: Optional[str]
    table_type: Optional[str] = Field(alias="tableType")

    dw_operation_set_id: Optional[int] = Field(alias='dwOperationSetId')
    dataset_dependencies: List[int] = Field(alias='datasetDependencies')

    column_count: Optional[int] = Field(alias='columnCount')
    consumer_count: Optional[int] = Field(alias='consumerCount')

    attributes: Optional[Dict[str, str]]
    tags: Optional[List[str]]

    create_timestamp: Optional[datetime] = Field(alias='createTimestamp')
    create_author: Optional[int] = Field(alias='createdBy')
    update_timestamp: Optional[datetime] = Field(alias='updateTimestamp')
    update_author: Optional[int] = Field(alias='updatedBy')
    source_type: Optional[str] = Field(alias='sourceType', default="RASGO")

    verified_user: Optional[user_schemas.NestedUser] = Field(alias="verifiedUser")
    verified_timestamp: Optional[datetime] = Field(alias="verifiedTimestamp")

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


class DatasetCreate(BaseModel):
    """
    Contract to accept in post endpoints
    """

    name: str
    resource_key: Optional[str] = Field(alias='resourceKey')
    description: Optional[str]
    dw_table_id: Optional[int] = Field(alias='dwTableId')
    dw_operation_set_id: Optional[int] = Field(alias='dwOperationSetId')
    attributes: Optional[Dict[str, str]]
    tags: Optional[List[str]]
    owner_emails: Optional[List[str]] = Field(alias="ownerEmails")
    source_type: Optional[str] = Field(alias='sourceType', default="RASGO")

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


class DatasetPublish(BaseModel):
    """
    Contract to accept in publish endpoints
    """

    resource_key: Optional[str] = Field(alis="resourceKey")
    operation_set_resource_key: str = Field(alias="operationSetResourceKey")
    terminal_operation_resource_key: Optional[str] = Field(alias='terminalOperationResourceKey')
    table_name: Optional[str] = Field(alias="tableName")
    table_type: Optional[str] = Field(alias="tableType", default="VIEW")
    source_type: Optional[str] = Field(alias="sourceType", default="RASGO")
    name: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    attributes: Optional[Dict[str, str]] = None
    owner_emails: Optional[List[str]] = Field(alias="ownerEmails")

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


class DatasetRePublish(BaseModel):
    """
    Contract to accept in re-publish endpoints
    """

    operation_set_resource_key: str = Field(alias="operationSetResourceKey")
    terminal_operation_resource_key: Optional[str] = Field(alias='terminalOperationResourceKey')
    table_type: Optional[str] = Field(alias="tableType", default="VIEW")
    source_type: Optional[str] = Field(alias="sourceType", default="RASGO")
    name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    attributes: Optional[Dict[str, str]] = None
    owner_emails: Optional[List[str]] = Field(alias="ownerEmails")

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


class DatasetUpdate(BaseModel):
    """
    Contract to accept in put endpoints
    """

    name: Optional[str]
    description: Optional[str]
    attributes: Optional[dict]
    tags: Optional[List[str]]
    owner_emails: Optional[List[str]] = Field(alias="ownerEmails")
    verified: Optional[bool]

    class Config:
        allow_population_by_field_name = True
