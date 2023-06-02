import requests # pip install requests

URL = 'http://localhost:8000/api/v1/reviews'




# ----------- GET ------------------


HEADERS = {
    'accept': 'application/json'
}
QUERYSET = {'page': 2, 'limit': 1}

response = requests.get(URL, headers = HEADERS, params = QUERYSET)

if response.status_code == 200:
    print('Petición realizada con éxito\n')

    #print(response.content)
    if response.headers.get('content-type') == 'application/json':
        reviews = response.json()
        for review in reviews:
            print(f"score: {review['score']} - {review['reviews']}")
    
    print('\n')
     
    print(response.headers)



# ------------ POST ---------------

REVIEW = {
    'user_id': 1,
    'movie_id': 2,
    'reviews': 'review creada con request',
    'score': 6
}

response_post = requests.post(URL, json = REVIEW)

if response.status_code == 200:
    print('Reseña creada con éxito')
    print(response.json()[0]["id"])
else:
    print(
        response.content
    )



# ------------ PUT & DELETE ---------------

REVIEW_ID_PUT = 1
URL2 = f'http://localhost:8000/api/v1/reviews/{REVIEW_ID_PUT}'

REVIEW_PUT = {
    'reviews': 'nueva review, actualizar contenido',
    'score': 1
}

response2 = requests.put(URL2, json = REVIEW_ID_PUT)

if response.status_code == 200:
    print('La reseña se actualizó con éxito')

    print(response.json())


REVIEW_ID_DELETE = 10
URL3 = f'http://localhost:8000/api/v1/reviews/{REVIEW_ID_DELETE}'

response3 = requests.delete(URL3)

if response3.status_code == 200:
    print('La reseña se eliminó con éxito')

    print(response3.json())
