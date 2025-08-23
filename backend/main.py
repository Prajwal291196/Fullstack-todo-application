from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

app = FastAPI()

# Security setup
security = HTTPBearer()
DUMMY_TOKEN = "secrettoken123"  # this is your "password" for now

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != DUMMY_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
        )
    return True

class Todo(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool = False
    
todos: list[Todo] = []

@app.get("/", status_code=200)
def read_root():
    return {"Hello": "World"}


@app.get("/todos", response_model=list[Todo], status_code=200)
def get_todos():
    return todos

@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(todo: Todo):
    todos.append(todo)
    return todo

@app.get("/todos/{todo_id}", response_model=Todo, status_code=200)
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")
    
@app.put("/todos/{todo_id}", response_model=Todo, status_code=200)
def update_todo(todo_id: int, updated_todo: Todo,  authorized: bool = Depends(verify_token)):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, authorized: bool = Depends(verify_token)):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return
    raise HTTPException(status_code=404, detail="Todo not found")
        