from fastapi import FastAPI,Depends,status,Response,HTTPException
from typing import Optional,List
from pydantic import BaseModel
from passlib.context import CryptContext
import uvicorn
from database import engine,SessionLocal
import schemas ,models ,schemas
from sqlalchemy.orm import Session




app = FastAPI()



models.Base.metadata.create_all(engine)




def get_db():
    db = SessionLocal()
    try:
        yield db
        
    finally:
        db.close()





@app.post('/create-blog',status_code=status.HTTP_201_CREATED,tags=['blogs'])
def blog(request:schemas.Blog,db:Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title,body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog






@app.put('/update-blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=['blogs'])
def update_blog(id,request:schemas.Blog,db:Session=Depends(get_db)):
    
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'bllog with this id {id} not exist')

    blog.update(request.dict())
    db.commit()
    return 'update'





@app.delete('/delete-blog/{id}/',status_code=status.HTTP_204_NO_CONTENT,tags=['blogs'])
def delete_blog(id,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.fisrt():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'bllog with this id {id} not exist')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'deleted'
    # if not blog:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'blog with this id {id} is not exist')





    
@app.get('/all-blog/',status_code=status.HTTP_200_OK,response_model=list[schemas.ShowBlog],tags=['blogs'])
def all_blogs(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs 





@app.get('/one-blog/{id}/',status_code=status.HTTP_200_OK,response_model=schemas.ShowBlog,tags=['blogs'])
def show_one(id,respone:Response ,db:Session=Depends(get_db)):
    blog= db.query(models.Blog).filter(models.Blog.id == id).first()
    # db.commit()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'blog with this id {id} in not available')
        # respone.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':f'blog with this id {id} in not available'}
    
    return blog






pwd_cxt=CryptContext(schemes=['bcrypt'],deprecated='auto')


@app.post('/create-user',tags=['users'])
def create_user(request:schemas.User,db:Session=Depends(get_db),tags=['users']):
    hashed_passwrod=pwd_cxt.hash(request.password)
    new_user=models.User(name=request.name,email=request.email,password=hashed_passwrod)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user




@app.get('/show-users',response_model=list[schemas.ShowUser],tags=['users'])
def show_user(db:Session=Depends(get_db)):
    users=db.query(models.User).all()
    return users




@app.get('/getuser/{id}',response_model=schemas.ShowUser,tags=['users'])
def get_user(id,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'user with this id {id} in not available')
    return user





if __name__ == '__main__':
    uvicorn.run(app,host='127.0.0.1',port=8000)