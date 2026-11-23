from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy import create_engine
from sqlalchemy import Column,String,Integer,Date
from sqlalchemy.orm import sessionmaker,Session,declarative_base
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt ,JWTError
from datetime import datetime,timedelta,timezone,date
from pydantic import BaseModel,EmailStr
from sqlalchemy import ForeignKey
from typing import Optional

from dotenv import load_dotenv
import os

load_dotenv()
ALGORITHM=os.getenv("algorithm")
DB_CONNECTION=os.getenv("db_connection")
SECRET_KEY=os.getenv("secret_key")
EXPIRY_TIME=30
#create engine
engine=create_engine(DB_CONNECTION)

#make session
session_local=sessionmaker(bind=engine)

#
base=declarative_base()

#create table for login
class user_detail(base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)

#create table for task
class TaskModel(base):
    __tablename__="task"
    id=Column(Integer,primary_key=True)
    title=Column(String,nullable=False)
    description=Column(String)   
    status=Column(String,nullable=False)
    due_date=Column(Date,nullable=False)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)#Foreign Key ka format hota hai "table_name.column_name"

#
base.metadata.create_all(bind=engine)

#db session provide 
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

app=FastAPI()

#hashing algorithm setup 
pwd_context=CryptContext(schemes="bcrypt",deprecated="auto")

#save hashpassword
def hash_password(password:str):
    return pwd_context.hash(password)

#token extraction from client
oauth_schema=OAuth2PasswordBearer(tokenUrl="login")

#verify password
def verify_password(plain_passowrd,hash_password):
    return pwd_context.verify(plain_passowrd,hash_password)

#create token
def create_token(data:dict):
    to_encode=data.copy()
    expiry_time=datetime.now(timezone.utc)+timedelta(minutes=EXPIRY_TIME)
    to_encode.update({"exp":expiry_time})
    token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token

#verify token
def verify_token(token:str=Depends(oauth_schema)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email=payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401,detail="email not found")
        return email
    except JWTError:
        raise HTTPException(status_code=401,detail="token Invalid")
    
#pydantic for user register
class user_register(BaseModel):
    name:str
    email:EmailStr
    password:str

#user register
@app.post("/register")
def register(user:user_register,db:Session=Depends(get_db)):
    existing_user=db.query(user_detail).filter(user_detail.email==user.email).first()
    name=user.name
    email=user.email
    password=user.password
    if existing_user:
        raise HTTPException(status_code=400,detail="email already exists")
    user_data=user_detail(name=name,email=email,password=hash_password(password))
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return {"message":"you have sucessfully registerd! "}

#user login
@app.post("/login")
def login(user_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(user_detail).filter(user_detail.email==user_data.username).first()
    if not user:
        raise HTTPException(status_code=404,detail="email not founds")
    if not verify_password(user_data.password,user.password):
        raise HTTPException(status_code=401,detail="unauthorised")
    token=create_token({"sub":user_data.username})
    return {"access_token":token,
            "token_type":"bearer"
            }

@app.get("/secure")
def secure(email=Depends(verify_token)):
    return{"message":"scure route acess","email":email}

class TaskCreate(BaseModel):
    title:str
    description:Optional[str]
    status:str
    due_date:date

@app.post("/create_task")
def create_task(task:TaskCreate,db:Session=Depends(get_db),email=Depends(verify_token)):
    title=task.title
    description=task.description
    status=task.status
    due_date=task.due_date
    current_user=db.query(user_detail).filter(user_detail.email==email).first()
    if current_user is None:
        raise HTTPException(status_code=404,detail="user not found")
    user=TaskModel(title=title,description=description,status=status,due_date=due_date,user_id=current_user.id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return{"message":"task sucessfully created! "}

@app.get("/get_task")
def get_task(db:Session=Depends(get_db),email=Depends(verify_token)):
    # if email is None:
    #     raise HTTPException(status_code=401,detail="unauthorised")
    current_user=db.query(user_detail).filter(user_detail.email==email).first()
    if current_user is None:
        raise HTTPException(status_code=404,detail="current user not found")
    data=db.query(TaskModel).filter(TaskModel.user_id==current_user.id).all()
    return data

@app.get("/get_task/{task_id}")
def get_task(task_id:int,db:Session=Depends(get_db),email=Depends(verify_token)):
    current_user=db.query(user_detail).filter(user_detail.email==email).first()
    if current_user is None:
        raise HTTPException(status_code=401,detail="current user not found")
    data=db.query(TaskModel).filter(TaskModel.user_id==current_user.id,task_id==TaskModel.id).first()
    if data is None:
        raise HTTPException(status_code=404,detail="Task not found")
    return data

class TaskUpdate(BaseModel):
    title:str
    description:Optional[str]=None
    status:str
    due_date:date
@app.put("/update/{task_id}")
def update_task(update_task:TaskUpdate,task_id:int,db:Session=Depends(get_db),email=Depends(verify_token)):
    current_user=db.query(user_detail).filter(user_detail.email==email).first()
    if current_user is None:
        raise HTTPException(status_code=404,detail="current user not found")
    data=db.query(TaskModel).filter(TaskModel.user_id==current_user.id,task_id==TaskModel.id).first()
    if data is None:
        raise HTTPException(status_code=404,detail="Task Not Found")
    data.title=update_task.title
    data.description=update_task.description
    data.status=update_task.status
    data.due_date=update_task.due_date
    db.commit()
    db.refresh(data)
    return {"message":"Task updated sucesssfully! "}

@app.delete("/task_delete/{task_id}")
def task_delete(task_id:int,db:Session=Depends(get_db),email=Depends(verify_token)):
    current_user=db.query(user_detail).filter(user_detail.email==email).first()
    if current_user is None:
        raise HTTPException(status_code=404,detail="current user not found")
    data=db.query(TaskModel).filter(TaskModel.user_id==current_user.id,task_id==TaskModel.id).first()
    if data is None:
        raise HTTPException(status_code=404,detail="Task is not found")
    db.delete(data)
    db.commit()
    return{"message":"Task deleted sucessfuly! "}

