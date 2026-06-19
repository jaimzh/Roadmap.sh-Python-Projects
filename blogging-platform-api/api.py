from typing import Optional

from fastapi import APIRouter, status, HTTPException
from models import PostInput, PostOutput
import services
import utils


router = APIRouter()

@router.post("/posts", response_model=PostOutput, status_code=status.HTTP_201_CREATED)
def create_post(post_input: PostInput):
    new_post = services.create_blog_post(
         title = post_input.title,
         content = post_input.content,
         category = post_input.category,
         tags =  post_input.tags
    )
    return new_post

@router.get("/posts", response_model=list[PostOutput], status_code=status.HTTP_200_OK)
def read_all_post(search_query:Optional[str] = None): 
    posts = services.get_all_blog_posts(search_query)
    return posts

@router.get("/posts/{post_id}", response_model=PostOutput)
def read_single_post(post_id: int): 
    post = services.get_blog_post(post_id)
    
    if not post: 
        raise HTTPException(status_code=404, detail="Blog post was not found")
    return post

@router.put("/posts/{post_id}", response_model=PostOutput, status_code=status.HTTP_200_OK)
def update_post(post_id:int, post_input:PostInput):
    post_by_id = services.get_blog_post(post_id)
    
    if not post_by_id: 
        raise HTTPException(status_code=404, detail="Blog post was not found by id ")
    
    updated_post = services.update_blog_post(
        post_id, 
        post_input.title,
        post_input.content, 
        post_input.category, 
        post_input.tags )
    
    return updated_post

@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id:int):
    post_was_deleted = services.delete_blog_post(post_id) #i mean it is a bool 
    
    if not post_was_deleted: 
        raise HTTPException(status_code=404, detail="Blog post was not found by id ")

    return None