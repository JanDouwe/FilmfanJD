from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route("/home")
def home():
    return render_template("home.html")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Je bent ingelogd!", category="succes")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Onjuiste inloggegevens, probeer het nog een keer.", category="error")
        else:
            flash("Onbekende inloggegevens.", category="error")

    session['no-reprint'] = True
    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Je bent uitgelogd", category="succes")

    session['no-reprint'] = True
    return redirect(url_for("auth.login"))

@auth.route("/sign-up", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Emailadres is al in gebruik.", category="error")
        elif len(email) < 8:
            flash("Email moet minimaal 5 karakters lang zijn", category="error")
        elif len(username) < 4:
            flash("Gebruikersnaam moet minimaal 4 karakters lang zijn", category="error")
        elif len(password1) <= 7:
            flash("Wachtwoord moet minimaal 8 karakters lang zijn", category="error")
        elif password1 != password2:
            flash("Wachtwoorden komen niet overeen", category="error")                    
        else:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash("Gebruikersnaam bestaat al, kies een andere gebruikersnaam")
            else:
                hashed_password = generate_password_hash(password1, method="scrypt")
                new_user = User(email=email, username=username, password=hashed_password)    
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash("Registratie succesvol!", category="success")
                return redirect(url_for("views.home"))
                    
    session['no-reprint'] = True    
    return render_template("sign_up.html", user=current_user)


