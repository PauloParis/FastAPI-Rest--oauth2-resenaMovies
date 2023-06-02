import requests

URL = 'http://localhost:8000/api/v1/users/'

USER = {
    'username': 'user3',
    'password': 'pass3'
}

response = requests.post(URL + 'login', json = USER)

if response.status_code == 200:
    print('Usuario autenticado de forma exitosa')

    #print(response.json())
    #print(response.cookies.get_dict())

    user_id = response.cookies.get_dict().get('user_id')
    print(user_id)


    # devolver las reviews que le pertenecen al user

    cookies = { 'user_id': user_id }
    response = requests.get(URL + 'reviews', cookies = cookies)

    if response.status_code == 200:
        for review in response.json():
            print(f"{review['reviews']} - {review['score']}")

