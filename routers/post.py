from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
import models, schema, oauth2
from typing import List

router = APIRouter()

# CRUD Operations of SQLALCHEMY

@router.post("/create_sqlalchemy_post",status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(post: schema.PostBase, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(title=post.title, content = post.content, published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return {"data": new_post}

@router.get("/one_sqlalchemy_posts/{id}")
def get_post(id: str, db: Session = Depends(get_db)):
    post2 = db.query(models.Post).filter(models.Post.id == id).first()
    if not post2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")
    return {"post_details": post2}

@router.delete("/delete_post_sqlalchemy/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):

    post_del = db.query(models.Post).filter(models.Post.id == id)
    if post_del.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with this id: {id} does not exist.")
 
    post_del.delete(synchronize_session = False)
    db.commit()

    return Response(status_code= status.HTTP_204_NO_CONTENT)
   
@router.put("/update_sql/{id}",response_model=schema.Post)
def update_post(id: int, updated_post: schema.PostBase, db: Session = Depends(get_db)):
    post_new = db.query(models.Post).filter(models.Post.id == id)
    post5 = post_new.first()
    if post5 == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with this id: {id} does not exist.")
    post_new.update(updated_post.model_dump(), synchronize_session= False)
    db.commit()
    return post_new.first()