from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'afafdgibgafgkuig'
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    with app.app_context():
        db.create_all()
        create_database(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    with app.app_context():
        if not path.exists("website/" + DB_NAME):
            db.create_all()

            from .models import Film, Director, Role, Actor, Extras
            if not Film.query.first():

                kruistocht = Film(
                    title="Kruistocht in spijkerbroek",
                    director=sombogaart,
                    release_year=2006,
                    image_filename="kruistocht in spijkerbroek.jpg"
                )
                kruistocht.extras = Extras(extra="Kruistocht in Spijkerbroek is gebaseerd op het gelijknamige boek van Thea Beckman. De vijftienjarige Dolf gebruikt een prototype van een tijdmachine en belandt tegen zijn wil in de Middeleeuwen. Hij wordt neergeslagen door overvallers, maar wordt gered door de mooie en stoere Jenne. Zij maakt deel uit van een kinderkruistocht, achtduizend kinderen die op weg zijn naar Jeruzalem om de stad te bevrijden van de Arabieren.")

                zwartboek = Film(
                    title="Zwartboek",
                    director=verhoeven,
                    release_year=2006,
                    image_filename="zwartboekposter.jpg"
                )
                zwartboek.extras = Extras(extra="In het laatste jaar van de tweede wereldoorlog wordt de verblijfplaats van de Joodse Rachel Stein gebombardeerd. Ze wordt opgevangen door een lokale zeiler en krijgt bezoek van Van Gein, die waarschuwt dat de Duitsers haar nieuwe adres kennen. Hij biedt haar een veilige doorgang door de Biesbosch naar het bevrijde zuiden van Nederland. Ontsnappen uit het bezette deel blijkt echter moeilijker dan gedacht.")

                saving_private_ryan = Film(
                    title="Saving Private Ryan",
                    director=spielberg,
                    release_year=1998,
                    image_filename="savingprivateryan.jpg"
                )
                saving_private_ryan.extras = Extras(extra="Tijdens de invasie van de Geallieerden in Normandië sterven twee broers. Een derde broer sterft gelijktijdig in Nieuw Guinea, bij het vechten tegen de Japanners. Als bekend wordt dat een vierde broer vermist is geraakt op het Franse platteland, wordt een missie gestart om hem veilig thuis te krijgen.")

                role1 = Role(actor=actor1, film=zwartboek, character_name="Rachel Stein")
                role2 = Role(actor=actor2, film=zwartboek, character_name="Ludwig Muntze")
                role3 = Role(actor=actor3, film=saving_private_ryan, character_name="Captain Miller")
                role4 = Role(actor=actor4, film=saving_private_ryan, character_name="Private Ryan")
                role5 = Role(actor=actor5, film=saving_private_ryan, character_name="Sergeant Horvath")
                role6 = Role(actor=actor6, film=kruistocht, character_name="Dolf Wega")
                role7 = Role(actor=actor7, film=kruistocht, character_name="Jenne")

                sombogaart = Director(first_name="Ben", last_name="Sombogaart")
                verhoeven = Director(first_name="Paul", last_name="Verhoeven")
                spielberg = Director(first_name="Steven", last_name="Spielberg")

                actor1 = Actor(first_name="Carice", last_name="van Houten")
                actor2 = Actor(first_name="Sebastian", last_name="Koch")
                actor3 = Actor(first_name="Tom", last_name="Hanks")
                actor4 = Actor(first_name="Matt", last_name="Damon")
                actor5 = Actor(first_name="Tom", last_name="Sizemore")
                actor6 = Actor(first_name="Johnny", last_name="Flynn")
                actor7 = Actor(first_name="Stephanie", last_name="Leonidas")
                db.session.add_all([sombogaart, verhoeven, spielberg, actor1, actor2, actor3, actor4, actor5, actor6, actor7,
                                   kruistocht, zwartboek, saving_private_ryan, role1, role2, role3, role4, role5, role6, role7])
                db.session.commit()

                print("Database aangemaakt en gegevens toegevoegd!")






