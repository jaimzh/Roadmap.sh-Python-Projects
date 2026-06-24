from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.schemas import TodoRequest, TodoResponse
from app.services import todo_service

# the prefix is well used as a substitute for / i mean instead of writng /todos route everwwhere we just set up a prefix
# 1. Initialize the Router
# The prefix means every single endpoint will automatically start with "/todos"
router = APIRouter(prefix="/todos", tags=["Todos Operations"])

STATIC_USER_ID = 1  # place holder for the id before we set up auth


# ENDPOINT: CREATE A TODO
# Route: POST /todos
@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo_data: TodoRequest, db: Session = Depends(get_db)):
    return todo_service.create_todo(db=db, todo_data=todo_data, user_id=STATIC_USER_ID)


# ENDPOINT: GET ALL TODOS
# Route: GET /todos
@router.get("/", response_model=List[TodoResponse], status_code=status.HTTP_200_OK)
def read_all_todos(db: Session = Depends(get_db)) -> List[TodoResponse]:
    return todo_service.get_all_todos(db=db, user_id=STATIC_USER_ID)


# ENDPOINT: GET A SINGLE TODO BY ID
# Route: GET /todos/{todo_id}
@router.get("/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = todo_service.get_todo_by_id(
        db=db, todo_id=todo_id, user_id=STATIC_USER_ID
    )
    if not db_todo:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_todo


# ENDPOINT: UPDATE A TODO
# Route: PUT /todos/{todo_id}
@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_data: TodoRequest,
    is_completed: bool = False,
    db: Session = Depends(get_db),
):
    updated_todo = todo_service.update_todo(
        db=db,
        todo_id=todo_id,
        todo_data=todo_data,
        is_completed=is_completed,
        user_id=STATIC_USER_ID,
    )
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_todo


# ENDPOINT: DELETE A TODO
# Route: DELETE /todos/{todo_id}
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    success = todo_service.delete_todo(db=db, todo_id=todo_id, user_id=STATIC_USER_ID)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None
