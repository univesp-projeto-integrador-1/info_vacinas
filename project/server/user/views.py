# project/server/user/views.py


from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from project.server import bcrypt, db
from project.server.models import User
from project.server.user.forms import LoginForm, RegisterForm

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/register", methods=["GET", "POST"])
@login_required
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash("Thank you for registering.", "success")
        return redirect(url_for("user.members"))

    return render_template("user/register.html", form=form)


@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
            user.password, request.form["password"]
        ):
            login_user(user)
            flash("Você foi autenticado com sucesso. Bem vindo!", "success")
            return redirect(url_for("user.members"))
        else:
            flash("Invalid email and/or password.", "danger")
            return render_template("user/login.html", form=form)
    return render_template("user/login.html", title="Please Login", form=form)


@user_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out. Bye!", "success")
    return redirect(url_for("main.home"))


@user_blueprint.route("/members")
@login_required
def members():
    return render_template("user/members.html")
