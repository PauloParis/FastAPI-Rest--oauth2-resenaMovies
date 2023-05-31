
from fastapi import FastAPI
from fastapi import HTTPException

from database import User
from database import Movie
from database import UserReview
from database import database as connection


from schemas import UserRequestModel
from schemas import UserResponseModel


# uvicorn main:app --reload -> levantar servidor --reload es como nodemon

app = FastAPI(title = 'Proyecto para reseñar peliculas',
              description = 'En este proyecto seresmioa capaces de reseñar peliculas',
              version = '1')



# -------------- Rutas -------------

@app.get('/')
async def index():
    return 'Hola mundo, desde un servidor en FastAPI'


@app.get('/about')
async def about():
    return 'About'


# ------------ Eventos -------------
@app.on_event('startup')
def startUp():
    print('El servidor va a comenzar')
    if connection.is_closed():
        connection.connect()
        print('conectando a database')
    
    connection.create_tables([User, Movie, UserReview]) # si ya existen, no pasa nada

@app.on_event('shutdown')
def shutDown():
    print('El servidor se encuentra finalizando...')
    if not connection.is_closed():
        connection.close()
        print('desconectando a database')




# ---------- Crear Usuario --------------

@app.post('/users', response_model = UserResponseModel)
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

