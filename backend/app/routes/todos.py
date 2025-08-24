from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoOut
from pydantic import BaseModel
from typing import List
from app.auth.jwt_handler import get_current_user

router = APIRouter(prefix="/todos", tags=["Todos"])

# In-memory todo list (dummy for now)
# todos = []

# Pydantic model for Todo
# class Todo(BaseModel):
#     id: int
#     task: str
#     completed: bool = False


# 📌 GET all todos (public)
@router.get("/", response_model=List[TodoOut])
def list_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()
# def get_todos():
#     return todos


# 📌 POST new todo (public for now)
@router.post("/", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate, db: Session = Depends(get_db)):
    todo = Todo(title=payload.title, completed=payload.completed)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo
# def add_todo(todo: Todo):
#     todos.append(todo)
#     return todo


# 📌 PUT update todo (protected)
@router.put("/{todo_id}", response_model=TodoOut )
def update_todo(todo_id: int, payload: TodoUpdate, db: Session = Depends(get_db), # current_user: dict = Depends(get_current_user)  # enable when ready
):
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    if payload.title is not None:
        todo.title = payload.title
    if payload.completed is not None:
        todo.completed = payload.completed

    db.commit()
    db.refresh(todo)
    return todo
# def update_todo(todo_id: int, updated_todo: Todo, user: dict = Depends(get_current_user)):
#     for idx, todo in enumerate(todos):
#         if todo.id == todo_id:
#             todos[idx] = updated_todo
#             return updated_todo
#     raise HTTPException(status_code=404, detail="Todo not found")


# 📌 DELETE todo (protected)
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    # current_user: dict = Depends(get_current_user)  # enable when ready
):
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return None
# def delete_todo(todo_id: int, user: dict = Depends(get_current_user)):
#     for idx, todo in enumerate(todos):
#         if todo.id == todo_id:
#             todos.pop(idx)
#             return {"message": "Todo deleted successfully"}
#     raise HTTPException(status_code=404, detail="Todo not found")
