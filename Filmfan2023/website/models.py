from website import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    username = db.Column(db.String(20), unique=True)
    extras = db.relationship("Extras", backref="user", lazy="dynamic")

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director", backref=db.backref("films"))
    release_year = db.Column(db.Integer)
    image_filename = db.Column(db.String(100))
    extras = db.relationship("Extras", backref="film", uselist=False)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey("actor.id"))
    actor = db.relationship("Actor", backref=db.backref("roles"))
    film_id = db.Column(db.Integer, db.ForeignKey("film.id"))
    film = db.relationship("Film", backref=db.backref("roles"))
    character_name = db.Column(db.String(100))      

class Extras(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey("film.id"), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    extra = db.Column(db.String(1000))


