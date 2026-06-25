from sqlalchemy.orm import Session
from app.models.db import Todo
from app.models.schemas import TodoRequest


# turn the request body into a real Todo row connected to the logged-in user
def create_todo(db: Session, todo_data: TodoRequest, user_id: int):
    new_todo = Todo(
        title=todo_data.title,
        description=todo_data.description,
        user_id=user_id,
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


# fetch only this user's todos, then slice them with page and limit
def get_all_todos(db: Session, user_id: int, page: int, limit: int):
    total_items = db.query(Todo).filter(Todo.user_id == user_id).count()
    skip = (page - 1) * limit
    todos = db.query(Todo) \
        .filter(Todo.user_id == user_id) \
        .offset(skip) \
        .limit(limit) \
        .all()

    return {
        "data": todos,
        "page": page,
        "limit": limit,
        "total": total_items
    }


# scoped lookup: only returns the todo if this user owns it
def get_todo_by_id(db: Session, todo_id: int, user_id: int):
    return db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()


# unscoped lookup: used before update/delete so we can tell 404 from 403
def get_todo_by_id_any_user(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()


# update only happens after the route has checked the user owns this todo
def update_todo(db: Session, todo_id: int, todo_data: TodoRequest, is_completed: bool, user_id: int):
    db_todo = get_todo_by_id(db, todo_id, user_id)
    if db_todo:
        db_todo.title = todo_data.title
        db_todo.description = todo_data.description
        db_todo.is_completed = is_completed
        db.commit()
        db.refresh(db_todo)

    return db_todo


# delete only happens after the route has checked the user owns this todo
def delete_todo(db: Session, todo_id: int, user_id: int):
    db_todo = get_todo_by_id(db, todo_id, user_id)
    if db_todo:
        db.delete(db_todo)
        db.commit()
        return True
    return False
