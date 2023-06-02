

from fastapi import APIRouter
from fastapi import HTTPException

from ..database import UserReview
from ..database import User
from ..database import Movie

from ..schemas import ReviewRequestModel
from ..schemas import ReviewResponseModel
from ..schemas import ReviewRequestPutModel

from typing import List



router = APIRouter(prefix='/reviews')



# ---------- Crear Reseña --------------

@router.post('', response_model = ReviewResponseModel)
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





# ----------- obtener reseñas ------------

@router.get('', response_model = List[ReviewResponseModel])
async def get_reviews(page: int = 1, limit: int = 10):
    reviews = UserReview.select().paginate(page, limit) # SELECT * FROM user_reviews
    # paginate (pagina actual, cantidad max de elementos)

    return [ user_review for user_review in reviews ]



# obtener una sola reseña
@router.get('/{id}', response_model = ReviewResponseModel)
async def get_review(id: int):
    review = UserReview.select().where(UserReview.id == id).first()

    if review is None:
        raise HTTPException(status_code = 404, detail = 'Review not found')

    return review


# actualizar reseña

@router.put('/{id}', response_model =  ReviewResponseModel)
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

@router.delete('/{id}', response_model = ReviewResponseModel)
async def delete_review(id: int):
    review = UserReview.select().where(UserReview.id == id).first()

    # no existe
    if review is None:
        raise HTTPException(status_code = 404, detail = 'Review not found')

    # si existe
    review.delete_instance() # de peewee
    
    return review



