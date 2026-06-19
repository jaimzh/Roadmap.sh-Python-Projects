from pydantic import BaseModel
from typing import List


#each blog post will have a title, content, category, and tags
class PostInput(BaseModel): 
    title: str
    content: str
    category: str
    tags: List[str]

#this validates the input data from postceate and if successful, it will return the data in the form of a post model
class PostOutput(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: List[str]
    created_at: str
    updated_at: str
