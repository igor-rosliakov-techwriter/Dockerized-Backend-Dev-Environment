from pydantic import BaseModel, Field

class TaskCreateRequest(BaseModel):
    title: str = Field(..., examples=["generate thumbnail"])

class TaskCreateResponse(BaseModel):
    task_id: int
    status: str
