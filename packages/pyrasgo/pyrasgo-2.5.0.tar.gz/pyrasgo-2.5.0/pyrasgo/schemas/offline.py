from datetime import datetime
from typing import Any, List, Optional, Dict

from pydantic_yaml import YamlModel, YamlStrEnum


class RasgoVersion(YamlStrEnum):
    V20 = '2.0'


class BaseV2(YamlModel):
    schema_version: RasgoVersion = RasgoVersion.V20

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class OfflineOperation(BaseV2):
    resource_key: Optional[str]
    operation_name: Optional[str]
    operation_type: Optional[str]
    operation_args: Optional[Dict[str, Any]]
    transform_name: Optional[str]
    dependencies: Optional[List[str]]
    fqtn: Optional[str]


class OfflineOperationSet(BaseV2):
    resource_key: Optional[str]
    operations: Optional[List[OfflineOperation]]
    dependencies: Optional[List[str]]
    sql: Optional[str]


class OfflineFilter(BaseV2):
    column_name: Optional[str]
    operator: Optional[str]
    comparison_value: Optional[str]


class OfflineMetric(BaseV2):
    name: Optional[str]
    type: Optional[str]
    target_expression: Optional[str]
    time_grains: Optional[List[str]]
    time_dimension: Optional[str]
    dimensions: Optional[List[str]]

    filters: Optional[List[OfflineFilter]]
    meta: Optional[Dict[str, str]]
    label: Optional[str]
    description: Optional[str]

    tags: Optional[List[str]]

    recent_values: Optional[List]
    recent_time_grain: Optional[str]
    recent_period_start: Optional[datetime]
    recent_period_end: Optional[datetime]


class OfflineColumn(BaseV2):
    name: Optional[str]
    data_type: Optional[str]


class OfflineDataset(BaseV2):
    name: Optional[str]
    resource_key: Optional[str]
    description: Optional[str]
    source_type: Optional[str] = "RASGO"
    organization_id: Optional[int]

    attributes: Optional[Dict[str, str]]
    tags: Optional[List[str]]

    dw_operation_set: Optional[OfflineOperationSet]
    columns: Optional[List[OfflineColumn]]
    metrics: Optional[List[OfflineMetric]]

    fqtn: Optional[str]


class OfflineTransformArgument(BaseV2):
    name: Optional[str]
    description: Optional[str]
    type: Optional[str]
    is_optional: Optional[bool]
    context: Optional[Dict[str, Any]]


class OfflineTransform(BaseV2):
    name: Optional[str]
    type: Optional[str]
    operation_type: Optional[str]
    description: Optional[str]
    arguments: Optional[List[OfflineTransformArgument]]
    tags: Optional[List[str]]
    context: Optional[Dict[str, Any]]
    dw_type: Optional[Optional[str]]
    is_accelerator: Optional[bool]
