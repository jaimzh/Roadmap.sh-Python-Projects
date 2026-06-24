from sqlalchemy.orm import Session
from app.models.db import Todo
from app.models.schemas import TodoRequest

# 1. CREATE A NEW TASK
def create_todo(db: Session, todo_data: TodoRequest, user_id: int):
    # We turn the abstract blueprint into a real row instance object
    new_todo = Todo(
        title=todo_data.title,
        description=todo_data.description,
        user_id=user_id  # Hardcoding the user link for now (we'll wire auth later!)
    )
    db.add(new_todo)       # Drop the new object into our isolated room container
    db.commit()            # Lock it into the todo.db file permanently
    db.refresh(new_todo)   # Refresh our object to grab the auto-generated database ID
    return new_todo        # Return the living instance (Pydantic will turn this to JSON!)


# 2. READ ALL TASKS FOR A USER
def get_all_todos(db: Session, user_id: int):
    # Using our arrow pointers! This runs a SELECT * WHERE user_id = user_id query
    return db.query(Todo).filter(Todo.user_id == user_id).all()


# 3. READ A SINGLE TASK BY ID
def get_todo_by_id(db: Session, todo_id: int, user_id: int):
    return db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()


# 4. UPDATE A TASK (Toggle completion or edit text)
def update_todo(db: Session, todo_id: int, todo_data: TodoRequest, is_completed: bool, user_id: int):
    # First, find the task in the room
    db_todo = get_todo_by_id(db, todo_id, user_id)
    if db_todo:
        db_todo.title = todo_data.title
        db_todo.description = todo_data.description
        db_todo.is_completed = is_completed  # Update the boolean status
        db.commit()                          # Save changes to the file
        db.refresh(db_todo)
    return db_todo


# 5. DELETE A TASK
def delete_todo(db: Session, todo_id: int, user_id: int):
    db_todo = get_todo_by_id(db, todo_id, user_id)
    if db_todo:
        db.delete(db_todo)  # Throw it out of the database room
        db.commit()         # Save the deletion permanently
        return True
    return False