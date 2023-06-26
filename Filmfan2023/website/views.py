from flask import Blueprint, render_template, request, redirect, url_for, request
from flask_login import login_required, current_user
from .models import db, Film, Director, Actor

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("home.html", user=current_user)

@views.route("/film_detail/<int:film_id>")
def film_details(film_id):
    film = Film.query.get(film_id)
    director = "Onbekend"
    if film.director:
        director = film.director.first_name + " " + film.director.last_name
    actors = [role.actor.first_name + " " + role.actor.last_name for role in film.roles]
    character_names = [role.character_name for role in film.roles]

    return render_template("film_detail.html", film=film, director=director, actors=actors, character_names=character_names)


@views.route("/film_detail/<int:film_id>", methods=["GET", "POST"])
def edit_film(film_id):
    film = Film.query.get(film_id)
    if not film:
        return "Film not found"

    if request.method == "POST":
        if current_user.is_authenticated:
            if "title" in request.form:
                film.title = request.form["title"]
            if "director" in request.form and request.form["director"]:
                director_names = request.form["director"].split()
                if len(director_names) >= 2:
                    first_name = director_names[0]
                    last_name = director_names[1]
                    if film.director:
                        film.director.first_name = first_name
                        film.director.last_name = last_name
                    else:
                        director = Director(first_name=first_name, last_name=last_name)
                        film.director = director
            if "release_year" in request.form:
                film.release_year = request.form["release_year"]
            if "extra" in request.form:
                film.extras.extra = request.form["extra"]
            if "actors" in request.form:
                selected_actors = request.form.getlist("actors")
                film.actors = Actor.query.filter(Actor.id.in_(selected_actors)).all()

            db.session.commit()
            return redirect(url_for("views.film_details", film_id=film_id))

    director = ""
    if film.director:
        director = film.director.first_name + " " + film.director.last_name
    else:
        director = "Onbekend"
    actors = [role.actor.first_name + " " + role.actor.last_name for role in film.roles]
    character_names = [role.character_name for role in film.roles]

    return render_template("film_detail.html", film=film, director=director, actors=actors, character_names=character_names)






