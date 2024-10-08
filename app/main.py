from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
  title: str
  content: str
  published: bool = True
  rating: Optional[int] = None

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
           {"title": "favorite foods", "content": "I like pizza", "id": 2}]

def find_post_index(id: int):
  for i, post in enumerate(my_posts):
    if post['id'] == id:
      return i
  return None


@app.get("/")
def root():
  return {"message": "welcome to my API"}

@app.get("/posts")
def get_posts():
  return {"data": my_posts}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
  post_found =  next(filter(lambda x: x['id'] == id, my_posts),None)
  if not post_found:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id } was not found")
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"message": f"post with id: {id} was not found"}

  return {"post_detail": post_found}
  

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
  post_dict = post.model_dump(mode="python")
  post_dict['id'] = randrange(0, 100000)
  my_posts.append(post_dict)
  return {"data": post_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
  index = find_post_index(id)
  if index is None:
    raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
  my_posts.pop(index)
  return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
  index = find_post_index(id)
  if index is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
  
  post_dict = post.model_dump(mode="python")
  post_dict['id'] = id
  my_posts[index] = post_dict
  return {"data": post_dict}

  