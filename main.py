from fastapi import FastAPI,Response,status,HTTPException,Depends
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from database import engine, get_db
import models, schema
from routers import post, user, auth
from config import settings

print(settings.database_username)

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password = 'Vishnu@2001', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection Sucessfully done")
        break
    except Exception as error:
        print("connection to database is failed")
        time.sleep(2)

my_posts = [{"title":"title of the post 1","content": "content of the post 1","id":1},
            {"title": "fav color", "content": "i like blue","id":2}
            ]

users = {
    "name" : "vishnu",
    "id" : 542,
    "Title" : "dev"
}

@app.get("/task")
def hello():
    return users

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"status" : posts}

@app.get("/post/all")
def get_posts():
    cursor.execute("""Select * from posts """)
    my_new_posts = cursor.fetchall()
    return {"data":my_new_posts}

@app.post("/createpost",status_code=status.HTTP_201_CREATED)
def create_posts(new_post:schema.PostBase):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0,10000)
    my_posts.append(post_dict)
    return {"data":post_dict}

def find_post(id):
    for i in my_posts:
        if i["id"] == id:
            return i
        
@app.get("/posts/{id}")
def get_post(id:int, response: Response):
    single_post = find_post(id)
    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"Message": f"post with id:{id} was not found"}
    return {"post_details": single_post}

def get_index_post(id):
    for i, n in enumerate(my_posts):
        if n['id'] == id:
            return i


@app.delete("/deletepost/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = get_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with this id: {id} does not exist.")
    my_posts.pop(index)
    print(my_posts)
    return {"message" : "post was succesfully delete"}

@app.put("/put/{id}")
def update_post(id:int,post:schema.PostBase):
    index = get_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with this id: {id} does not exist.")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data":post_dict}


# CRUD Operations of DATABASE

@app.post("/create_database_post",status_code=status.HTTP_201_CREATED)
def create_posts(new_post:schema.PostBase):
    cursor.execute(""" insert into posts (title, content, published) values(%s,%s,%s) returning * """,(new_post.title,new_post.content,new_post.published))
    post_new = cursor.fetchone()
    conn.commit()
    return {"data":post_new}

@app.get("/one_posts/{id}")
def get_post(id: str):
    cursor.execute(""" SELECT * from posts WHERE id = %s """, (str(id),))
    single_post = cursor.fetchone()
    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")
    return {"post_details": single_post}

@app.delete("/delete_post_database/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s returning * """, (str(id),))
    delete_post = cursor.fetchone()
    conn.commit()
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with this id: {id} does not exist.")
    my_posts.pop(delete_post)
    print(my_posts)
    return {"message" : "post was succesfully delete"}

@app.put("/update_database/{id}")
def update_post(id: int, post1: schema.PostBase):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s RETURNING * """, (post1.title,post1.content,post1.published,str(id),))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with this id: {id} does not exist.")
    return {"data": updated_post}

