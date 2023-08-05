# -*- coding: utf-8 -*-
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

from pyrasgo.schemas.enums import OperationSetAsyncTaskType


class AsyncUpdateTask(BaseModel):
    id: int
    event_type: OperationSetAsyncTaskType = Field(alias='eventType')
    create_timestamp: datetime = Field(alias='createTimestamp')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
