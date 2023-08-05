from typing import Any, Optional
from pydantic import BaseModel


class Attribute(BaseModel):
    key: str
    value: Optional[Any]
