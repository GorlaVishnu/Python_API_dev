from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None
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

@app.get("/post/all")
def get_posts():
    cursor.execute("""Select * from posts """)
    my_new_posts = cursor.fetchall()
    return {"data":my_new_posts}

@app.post("/createpost",status_code=status.HTTP_201_CREATED)
def create_posts(new_post:post):
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
def update_post(id:int,post:post):
    index = get_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with this id: {id} does not exist.")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data":post_dict}

