from pydantic import BaseModel

class TodoBase(BaseModel):
    title: str
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

class TodoOut(TodoBase):
    id: int
    class Config:
        from_attributes = True  # Pydantic v2: replaces orm_mode
