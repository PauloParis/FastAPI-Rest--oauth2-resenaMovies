
""" 
definir los modelos para validar los datos de entrada o salida

"""

from pydantic import BaseModel
from pydantic import validator

from pydantic.utils import GetterDict

from typing import Any

from peewee import ModelSelect


# --------------- usuario ---------------

# convertir objeto a diccionario
class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):

        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)

        return res

class UserRequestModel(BaseModel):
    # será obligatorio enviar estos datos
    username: str
    password: str

    @validator('username')
    def username_validator(cls, username):
        if len(username) < 3 or len(username) > 10:
            raise ValueError('La longitud debe ser < 3 o > 10')
        
        return username
        

# se generan respuesta de tipo usuario
# valores a enviar
class UserResponseModel(BaseModel):
    id: int
    username: str


    # serializar el objeto de tipo model
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict



# --------------- reseña ---------------


# ----- validador de score -----
class ReviewValidator():

    @validator('score')
    def score_validator(cls, score):
        if score < 1 or score > 10:
            raise ValueError('La longitud de score debe ser >= 1 o <= 10')

        return score


class ReviewRequestModel(BaseModel, ReviewValidator):
    # datos obligatorios
    user_id: int
    movie_id: int
    reviews: str
    score: int

    

class ReviewResponseModel(BaseModel):
    id: int
    movie_id: int
    reviews: str
    score: int


    # serializar el objeto de tipo model
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict




# --------------- movie ---------------

class MovieRequestModel(BaseModel):
    title: str

class MovieResponseModel(BaseModel):
    id: int
    title: str
    
    # serializar el objeto de tipo model
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict



# validar datos de entrada para actualizar una reseña
class ReviewRequestPutModel(BaseModel, ReviewValidator):
    reviews: str
    score: int

    
    

