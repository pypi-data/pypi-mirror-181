"""
API Contracts for Data Warehouse Operations
"""
from typing import Dict, List, Optional, Any

from pydantic import BaseModel, Field

from pyrasgo.schemas import dw_table as dw_table_schemas


class OperationCreate(BaseModel):
    """
    Contract to create an Operation on set
    """

    operation_name: str = Field(alias='operationName')
    transform_id: Optional[int] = Field(alias='transformId')
    operation_args: Dict = Field(alias='operationArgs')
    sql_alias: Optional[str] = Field(alias="sqlAlias")

    def __eq__(self: 'OperationCreate', other: Any) -> bool:
        """
        Comparison to determine if an OperationCreate is same as another

        Returns True if Equals; False Otherwise
        """
        # If the other class isn't a OperationCreate return comparison error
        if not isinstance(other, OperationCreate):
            return False
        return (
            self.operation_name == other.operation_name
            and self.operation_args == self.operation_args
            and self.transform_id == other.transform_id
            and self.sql_alias == other.sql_alias
        )

    class Config:
        allow_population_by_field_name = True


class OperationUpdate(BaseModel):
    """
    Contract to update an Operation on set
    """

    operation_name: Optional[str] = Field(alias='operationName')
    transform_id: Optional[int] = Field(alias='transformId')
    operation_args: Optional[Dict] = Field(alias='operationArgs')
    sql_alias: Optional[str] = Field(alias="sqlAlias")

    class Config:
        allow_population_by_field_name = True


class Operation(BaseModel):
    """
    Contract representing a Operation
    """

    id: Optional[int]
    resource_key: Optional[str] = Field(alias='resourceKey')
    operation_name: Optional[str] = Field(alias='operationName')
    operation_type: Optional[str] = Field(alias='operationType')
    operation_args: Optional[dict] = Field(alias='operationArgs')
    operation_sql: Optional[str] = Field(alias='operationSQL')
    sql_alias: Optional[str] = Field(alias="sqlAlias")
    transform_id: Optional[int] = Field(alias='transformId')
    dw_operation_set_id: Optional[int] = Field(alias='dwOperationSetId')
    dependencies: Optional[List[str]]

    class Config:
        allow_population_by_field_name = True
