from fastapi import APIRouter, HTTPException, Query, status, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.schemas import PaginatedTodoResponse, TodoRequest, TodoResponse
from app.services import todo_service
from app.models import  db
from app.models.db import Todo
from app.utils.security import get_current_user

router = APIRouter(prefix="/todos", tags=["Todos Operations"])



@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo_data: TodoRequest, 
    db: Session = Depends(get_db), 
    current_user: db.User = Depends(get_current_user)
):
    return todo_service.create_todo(db=db, todo_data=todo_data, user_id=current_user.id)


 
@router.get("/", response_model=PaginatedTodoResponse, status_code=status.HTTP_200_OK)
def read_all_todos(
    db: Session = Depends(get_db),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    current_user: db.User = Depends(get_current_user) # Inject here
):
    # Swap STATIC_USER_ID for current_user.id
    return todo_service.get_all_todos(db=db, 
        user_id=current_user.id, 
        page=page, 
        limit=limit)


#
@router.get("/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def read_todo(
    todo_id: int, 
    db: Session = Depends(get_db),
    current_user: db.User = Depends(get_current_user) # Inject here
):
    # Swap STATIC_USER_ID for current_user.id
    db_todo = todo_service.get_todo_by_id(
        db=db, todo_id=todo_id, user_id=current_user.id
    )
    if not db_todo:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_todo



@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_data: TodoRequest,
    is_completed: bool = False,
    db: Session = Depends(get_db),
    current_user: db.User = Depends(get_current_user) # Inject here
):
    # Swap STATIC_USER_ID for current_user.id
    updated_todo = todo_service.update_todo(
        db=db,
        todo_id=todo_id,
        todo_data=todo_data,
        is_completed=is_completed,
        user_id=current_user.id,
    )
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_todo



@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int, 
    db: Session = Depends(get_db),
    current_user: db.User = Depends(get_current_user) # Inject here
):
    # Swap STATIC_USER_ID for current_user.id
    success = todo_service.delete_todo(db=db, todo_id=todo_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None



