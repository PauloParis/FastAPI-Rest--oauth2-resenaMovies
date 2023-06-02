
from fastapi import APIRouter
from fastapi import HTTPException

from ..database import Movie

from ..schemas import MovieRequestModel
from ..schemas import MovieResponseModel

router = APIRouter(prefix='/movies')

# ---------- Crear Movie --------------

@router.post('', response_model = MovieResponseModel)
async def create_movie(movie: MovieRequestModel):

    if Movie.select().where(Movie.title == movie.title).exists():
        return HTTPException(409, 'La pelicula ya existe')

    movie = Movie.create(
        title = movie.title
    )

    return movie

