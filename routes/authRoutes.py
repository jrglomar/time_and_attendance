from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from database import get_db
from models.userModel import User
from schemas.authSchema import TokenData, AuthForm
from schemas.userSchema import CreateUser
from jose import jwt
from passlib.context import CryptContext

secret = 'a very shady secret'
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def password_verify(plain, hashed):
    return pwd_context.verify(plain, hashed)

def password_hash(password):
    return pwd_context.hash(password)

router = APIRouter(
    prefix='/time_and_attendance/api/auth',
    tags=['auth']
)

@router.post('/register')
def register(request: CreateUser, db: Session = Depends(get_db)):
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

@router.post('/verify')
def verify(form: AuthForm, response: Response, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == form.email).first()
        if user:
            match = password_verify(form.password, user.password)
            if match:
                data = TokenData(email = user.email, id = user.id)
                token = jwt.encode(dict(data), secret)
                response.set_cookie('token', token, httponly=True)
                return {'user':user, 'message': 'Log In Success!'}
        
        return {'message': 'User not found.'}
    except Exception as e:
        print(e)

@router.post('/logout')
def logout(response: Response):
    response.delete_cookie('token')
    response.delete_cookie('id')
    response.delete_cookie('email')
    response.delete_cookie('type')
    return {'message': 'Logout Success!'}