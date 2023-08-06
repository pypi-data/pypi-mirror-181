from typing import Sequence, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class Page(BaseModel):
    items: Sequence[T]
    total: int
    page: int
    size: int

    class Config:
        orm_mode = True


all = [
    "Page"
]
