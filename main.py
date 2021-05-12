from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

blogPosts = [
    {"id": 1, "title": "First Post", "published": False},
    {"id": 2, "title": "Second Post", "published": True},
    {"id": 3, "title": "Third Post", "published": False},
    {"id": 4, "title": "Fourth Post", "published": True},
    {"id": 5, "title": "Fifth Post", "published": False},
]


@app.get('/blog')
def index(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {"message": f"{limit} published blog posts from the database", "data": blogPosts}
    else:
        return {"message": f"{limit} blog posts from the database", "data": blogPosts}


@app.get('/blog/unpublished')
def unpublished():
    return "unpublished"


@app.get('/blog/{id}')
def show(id: int):
    return {"data": id}


class Post(BaseModel):
    title: str
    published: Optional[bool]


@app.post('/blog')
def create_blog_post(post: Post):
    newPost: Post = {
        "id": len(blogPosts) + 1,
        "title": post.title,
        "published": post.published or False
    }
    print(newPost)
    blogPosts.append(newPost)
    return {"message": "Created", "data": blogPosts}
