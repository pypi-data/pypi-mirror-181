from enum import Enum


class OperationSetAsyncTaskType(str, Enum):
    FORK = "FORK"
    REVALIDATE = "REVALIDATE"
    UPDATE = "UPDATE"
    ACCELERATE = "ACCELERATE"


class DataWarehouseType(Enum):
    """
    Supported Data Warehouses
    """

    BIGQUERY = "bigquery"
    SNOWFLAKE = "snowflake"
