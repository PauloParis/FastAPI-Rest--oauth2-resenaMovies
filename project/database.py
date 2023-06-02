
from peewee import * #orm
from datetime import datetime
import hashlib

database = MySQLDatabase('fastapi_01',
                         user = 'root', 
                         password = 'PAULO1234',
                         host = 'localhost',
                         port = 3306)




# ---------- Modelos --------------

class User(Model):
    #atributos
    username = CharField(max_length=50, unique= True)
    password = CharField(max_length=50)
    created_at = DateTimeField(default = datetime.now)

    def __str__(self) -> str:
        return self.username
    
    class Meta:
        database = database
        table_name = 'users' # nombre de la tabla

    # hashear la contraseña
    @classmethod
    def create_password(cls, password):
        h = hashlib.md5()
        h.update(password.encode('utf-8'))
        return h.hexdigest()
    


    # OAUTH
    @classmethod
    def authenticate(cls, username, password):
        user = cls.select().where(User.username == username).first()

        if user and user.password == cls.create_password(password):
            return user



class Movie(Model):
    # atributos
    title = CharField(max_length=50)
    created_at = DateTimeField(default = datetime.now)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        database = database
        table_name = 'movies' # nombre de la tabla


class UserReview(Model):
    # atributos
    user = ForeignKeyField(User, backref='reviews')
    movie =  ForeignKeyField(Movie, backref='reviews')
    reviews = TextField()
    score = IntegerField()
    created_at = DateTimeField(default = datetime.now)


    def __str__(self) -> str:
            return f'{self.user.name} - {self.movie.title}'
    
    class Meta:
        database = database
        table_name = 'user_reviews' # nombre de la tabla

