from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from app.auth.jwt_handler import get_current_user

router = APIRouter()

# In-memory todo list (dummy for now)
todos = []

# Pydantic model for Todo
class Todo(BaseModel):
    id: int
    task: str
    completed: bool = False


# 📌 GET all todos (public)
@router.get("/todos", response_model=List[Todo])
def get_todos():
    return todos


# 📌 POST new todo (public for now)
@router.post("/todos", response_model=Todo)
def add_todo(todo: Todo):
    todos.append(todo)
    return todo


# 📌 PUT update todo (protected)
@router.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: Todo, user: dict = Depends(get_current_user)):
    for idx, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[idx] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="Todo not found")


# 📌 DELETE todo (protected)
@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, user: dict = Depends(get_current_user)):
    for idx, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(idx)
            return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")
