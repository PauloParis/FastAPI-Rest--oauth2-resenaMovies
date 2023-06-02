
from fastapi import FastAPI
from fastapi import APIRouter


from project.database import User
from project.database import Movie
from project.database import UserReview
from project.database import database as connection


from .routers import user_router
from .routers import movie_router
from .routers import review_router



# uvicorn main:app --reload -> levantar servidor --reload es como nodemon

app = FastAPI(title = 'Proyecto para reseñar peliculas',
              description = 'En este proyecto seresmioa capaces de reseñar peliculas',
              version = '1')


api_v1 = APIRouter(prefix='/api/v1')

api_v1.include_router(user_router)
api_v1.include_router(movie_router)
api_v1.include_router(review_router)

app.include_router(api_v1)

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









