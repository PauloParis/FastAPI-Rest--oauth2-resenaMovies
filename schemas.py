
""" 
definir los modelos para validar los datos de entrada o salida

"""

from pydantic import BaseModel
from pydantic import validator

from pydantic.utils import GetterDict

from typing import Any

from peewee import ModelSelect

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


    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict