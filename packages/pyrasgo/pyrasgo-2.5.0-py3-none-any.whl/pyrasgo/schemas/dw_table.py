from typing import Optional, List

from pydantic import BaseModel, Field


class DataColumn(BaseModel):
    """
    Contract to nest in a DataTable
    """

    id: Optional[int]
    column_name: Optional[str] = Field(alias='columnName')
    data_type: Optional[str] = Field(alias='dataType')

    class Config:
        allow_population_by_field_name = True


class DataTable(BaseModel):
    """
    Contract to nest in a Dataset
    """

    id: Optional[int]
    table_name: Optional[str] = Field(alias='tableName')
    database_name: Optional[str] = Field(alias='databaseName')
    schema_name: Optional[str] = Field(alias='schemaName')
    fqtn: Optional[str]
    table_type: Optional[str] = Field(alias='tableType', default="VIEW")

    class Config:
        allow_population_by_field_name = True


class DataTableWithColumns(DataTable):
    """
    Contract to nest in an OperationSet
    """

    columns: Optional[List[DataColumn]]
