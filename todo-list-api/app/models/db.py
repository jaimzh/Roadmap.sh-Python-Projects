from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from  app.database import Base


class User(Base): 
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    #think of this like a poiniter arrow to link to the other table, it points to a list of tasks
    todos = relationship("Todo", back_populates="owner", cascade="all, delete-orphan")
    #back populates means if you  edit todo.owner it will also edit  Users here, the cascade is a way to make sure that if a user is deleted all their tasks are delelted 
    #it is todo.owner and not Todo.owner because we are gonna make an object 
    
class Todo(Base): 
    __tablename__ = "todos"
    id = Column(Integer, primary_key="True", index=True)
    title = Column(String, nullable=False)
    description =Column(String, nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    #this points to the single user who owns this task by noticing the foreign key 
    owner = relationship("User", back_populates="todos")
    #back populaltes  if user.todos should change it affects Todo