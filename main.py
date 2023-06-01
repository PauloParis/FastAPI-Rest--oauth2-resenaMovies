
from fastapi import FastAPI
from fastapi import HTTPException

from database import User
from database import Movie
from database import UserReview
from database import database as connection


from schemas import UserRequestModel
from schemas import UserResponseModel

from schemas import ReviewRequestModel
from schemas import ReviewResponseModel

from schemas import MovieRequestModel
from schemas import MovieResponseModel

from typing import List

from schemas import ReviewRequestPutModel

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



# ---------- Crear Reseña --------------

@app.post('/reviews', response_model = ReviewResponseModel)
async def create_reviews(user_review: ReviewRequestModel):

    # validando si existe el usuario
    if User.select().where(User.id == user_review.user_id).first() is None:
        raise HTTPException(status_code = 404, detail = 'User not found')
    
    # validando si existe la pelicula
    if Movie.select().where(Movie.id == user_review.movie_id).first() is None:
        raise HTTPException(status_code = 404, detail = 'Movie not found')
    
    
    user_review = UserReview.create(
        user_id = user_review.user_id,
        movie_id = user_review.movie_id,
        reviews = user_review.reviews,
        score = user_review.score
    )

    return user_review


# ---------- Crear Movie --------------

@app.post('/movie', response_model = MovieResponseModel)
async def create_movie(movie: MovieRequestModel):

    movie = Movie.create(
        title = movie.title
    )

    return movie




# ----------- obtener reseñas ------------

@app.get('/reviews', response_model = List[ReviewResponseModel])
async def get_reviews():
    reviews = UserReview.select() # SELECT * FROM user_reviews

    return [ user_review for user_review in reviews ]


# obtener una sola reseña
@app.get('/reviews/{id}', response_model = ReviewResponseModel)
async def get_review(id: int):
    review = UserReview.select().where(UserReview.id == id).first()

    if review is None:
        raise HTTPException(status_code = 404, detail = 'Review not found')

    return review


# actualizar reseña

@app.put('/reviews/{id}', response_model =  ReviewResponseModel)
async def update_review(id: int, review_request: ReviewRequestPutModel):
    review = UserReview.select().where(UserReview.id == id).first()

    # no existe
    if review is None:
        raise HTTPException(status_code = 404, detail = 'Review not found')

    # si existe
    review.reviews = review_request.reviews
    review.score = review_request.score

    review.save()

    return review


# eliminar reseña

@app.delete('/reviews/{id}', response_model = ReviewResponseModel)
async def delete_review(id: int):
    review = UserReview.select().where(UserReview.id == id).first()

    # no existe
    if review is None:
        raise HTTPException(status_code = 404, detail = 'Review not found')

    # si existe
    review.delete_instance() # de peewee
    
    return review





