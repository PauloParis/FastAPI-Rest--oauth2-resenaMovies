from fastapi import APIRouter
from fastapi import HTTPException

from ..database import User

from ..schemas import UserRequestModel
from ..schemas import UserResponseModel


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