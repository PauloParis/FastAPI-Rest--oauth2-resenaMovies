import jwt

from datetime import datetime
from datetime import timedelta

from fastapi.security import OAuth2PasswordBearer


from .database import User
from fastapi import Depends


from fastapi import HTTPException
from fastapi import status



SECRET_KEY = 'sakHiJLb7RTK6'

oauth_schema = OAuth2PasswordBearer(tokenUrl = '/api/v1/auth')

def create_access_token(user, days = 7):
    data = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(days = days) # second = days  # fecha actual + 7 dias
    }

    return jwt.encode(data, SECRET_KEY, algorithm = 'HS256')




def decode_access_token(token):
    
    try: 
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except Exception as e: # error, por ejemplo que haya expirado el token
        return None

def get_current_user(token: str = Depends(oauth_schema)) -> User:
    data = decode_access_token(token)

    print(data)
    
    if data: 
        return User.select().where(User.id == data['user_id']).first()
    else:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Access Token no válido',
            headers = { 'WWWW-Autenticate': 'Bearer' }
        )