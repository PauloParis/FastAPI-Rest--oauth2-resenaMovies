from fastapi import APIRouter
from fastapi import HTTPException

from ..database import User

from ..schemas import UserRequestModel
from ..schemas import UserResponseModel


from fastapi.security import HTTPBasicCredentials #login


from fastapi import Response # cookies login
from fastapi import Cookie # cookies login


from typing import List
from ..schemas import ReviewResponseModel


from fastapi import Depends
from ..common import oauth_schema
from ..common import get_current_user


router = APIRouter(prefix='/users')


# ---------- Crear Usuario --------------

@router.post('', response_model = UserResponseModel)
async def create_user(user: UserRequestModel):
    
    if User.select().where(User.username == user.username).exists():
        return HTTPException(409, 'El username ya existe')

    hash_password = User.create_password(user.password)

    user = User.create(
        # estos datos vienen del archivo schemas
        username = user.username, 
        password = hash_password
    )

    #return UserResponseModel(id = user.id, username = user.username)
    return user  # se usa PeeweeGetterDict





# --------- login ----------

@router.post('/login', response_model = UserResponseModel)
async def login(credentials: HTTPBasicCredentials, response: Response):
    
    user = User.select().where(User.username == credentials.username).first()

    if user is None:
        raise HTTPException(404, 'User not found')
    
    if user.password != User.create_password(credentials.password):
        raise HTTPException(404, 'Password error')


    response.set_cookie(key = 'user_id', value = user.id)

    return user


# traer las review de un user autenticado - cookie
""" @router.get('/reviews', response_model = List[ReviewResponseModel])
async def get_reviews(user_id: int = Cookie(None)): 
    
    user = User.select().where(User.id == user_id).first()

    if user is None:
        raise HTTPException(404, 'User not found')
    
    return [ user_review for user_review in user.reviews ]

 """


# traer las review de un user autenticado - jwt
@router.get('/reviews',  response_model = List[ReviewResponseModel])
async def get_reviews(user: User = Depends(get_current_user)):  # token: str = Depends(oauth_schema) -> antiguo
    
    """ return {
        'token': token
    } -> antiguo """

    """ return {
        'id': user.id,
        'username': user.username
    } """

    return [ user_review for user_review in user.reviews ]