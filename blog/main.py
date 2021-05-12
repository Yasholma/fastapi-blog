from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.param_functions import Body
from sqlalchemy.orm import Session
from . import schemas, models
from .database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def findOrFail(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id: {id} not found")
    return blog


@app.get('/blog')
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return {"message": "All blogs fetched successfully", "data": blogs}


@app.get('/blog/{id}', status_code=status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    blog = findOrFail(id, db)
    return {"message": "Blog fetched successfully", "data": blog}


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(req: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=req.title, body=req.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"message": "Blog created successfully", "data": new_blog}


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)) -> None:
    blog = findOrFail(id, db)
    blog.delete(synchronize_session=False)
    db.commit()


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, req: schemas.Blog, db: Session = Depends(get_db)):
    blog = findOrFail(id, db)
    blog.update({"title": req.title, "body": req.body},
                synchronize_session=False)
    db.commit()
    return "updated"
