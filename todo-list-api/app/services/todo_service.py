from sqlalchemy.orm import Session
from app.models.db import Todo
from app.models.schemas import TodoRequest


#rule of thumb anything from the database has pascal casing then from python it has snake casing, Todo is from db and todo is what we are passing or manipulating in python code 
def create_todo(db: Session, todo_data: TodoRequest, user_id: int): 
    #we convert the well maybe abstract json blueprint into a real row instance object 
    new_todo = Todo(
        title=todo_data.title,
        description = todo_data.description,
        user_id = user_id #hardcoding the user id for now later on we'll hook it up to auth and make it automatic 
    )
    
    db.add(new_todo) #add the new object into a db
    db.commit()
    db.refresh(new_todo)
    return new_todo



# def get_all_todos(db:Session, user_id: int): 
#     # SELECT * FROM todos WHERE todos.user_id = 1; the reason it is one is just for now i mean a fixed placeholder 
#     return db.query(Todo).filter(Todo.user_id == user_id).all()





#pagination logic 

def get_all_todos(db: Session, user_id: int, page: int, limit: int):
    # 1. Get total count of items belonging to this user
    total_items = db.query(Todo).filter(Todo.user_id == user_id).count()
    
    # 2. Calculate offset math
    skip = (page - 1) * limit
    
    # 3. Fetch the specific slice of rows
    todos = db.query(Todo)\
              .filter(Todo.user_id == user_id)\
              .offset(skip)\
              .limit(limit)\
              .all()
              
    return {
        "data": todos,
        "page": page,
        "limit": limit,
        "total": total_items
    }
    
    
    
    
def get_todo_by_id(db:Session, todo_id: int,  user_id: int): 
    
    return db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()

def update_todo(db:Session, todo_id: int, todo_data: TodoRequest, is_completed: bool,   user_id: int):
    
    
    #first find the task by id
    db_todo = get_todo_by_id(db, todo_id,  user_id)
    #then do some patch work assignment 
    if db_todo: 
        db_todo.title = todo_data.title 
        db_todo.description = todo_data.description
        db_todo.is_completed = is_completed
        db.commit()
        db.refresh(db_todo)
        
    return db_todo

def delete_todo(db:Session, todo_id: int, user_id:int):
    db_todo = get_todo_by_id(db, todo_id,  user_id)
    if db_todo: 
        db.delete(db_todo)
        db.commit()
        return True
    return False
    
    
    