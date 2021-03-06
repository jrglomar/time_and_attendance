from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.userSchema import CreateUser
from models.userModel import User
from database import get_db
from jose import jwt
from passlib.context import CryptContext

secret = 'a very shady secret'
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def password_verify(plain, hashed):
    return pwd_context.verify(plain, hashed)

def password_hash(password):
    return pwd_context.hash(password)

router = APIRouter(
    prefix='/time_and_attendance/api/user',
    tags=['user']
)

@router.get('/')
def all(db: Session = Depends(get_db)):
    user = db.query(User).filter(User.active_status == "Active").all()
    return {'user': user}

@router.get('/{id}')
def read(id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(404, 'User not found')
    return {'user': user}

@router.get('/count/')
def count(db: Session = Depends(get_db)):
    count = db.query(User).filter(User.active_status == "Active").count()
    return {'count': count}

@router.post('/')
def store(request: CreateUser, db: Session = Depends(get_db)):
    try:
        request.password = password_hash(request.password)
        if request.user_type_id == "" or request.user_type_id == "string":
            user = User(
            email = request.email,
            password = request.password
        )
        else:
            user = User(
                user_type_id = request.user_type_id,
                email = request.email,
                password = request.password
            )
        db.add(user)
        db.commit()
        return {'message': 'Registered Successfully!'}
    except Exception as e:
        print(e)

@router.put('/{id}')
def update(id: str, user: CreateUser, db: Session = Depends(get_db)): 
    user.password = password_hash(user.password)
    if not db.query(User).filter(User.id == id).update({
        'user_type_id': user.user_type_id,
        'email': user.email,
        'password': user.password
    }):
        raise HTTPException(404, 'User to update is not found')
    db.commit()
    return {'message': 'User updated successfully.'}

@router.put('/delete/{id}')
def remove(id: str,  db: Session = Depends(get_db)):
    if not db.query(User).filter(User.id == id).update({
        'active_status': "Inactive",
    }):
        raise HTTPException(404, 'User to delete is not found')
    db.commit()
    return {'message': 'User removed successfully.'}

