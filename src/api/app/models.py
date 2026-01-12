from pydantic import BaseModel, Field
from uuid import UUID


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class TaskOut(BaseModel):
    id: UUID
    title: str
    status: str
