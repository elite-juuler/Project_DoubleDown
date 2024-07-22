from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import requests
import json

app = Flask(__name__)
app.secret_key = "Mko09ijn"
app.permanent_session_lifetime = timedelta(days=2)

# what is returned when url "/home" is navigated
@app.route("/")
def home():
    return render_template("index.html")

# when url "/home/" is navigated to, redirects user to actual "home" function
@app.route("/home/")
def direct_home():
    return redirect(url_for("home")) # with option to specify argument , param=""

## says hello to whatever url is navigated to
# @app.route("/<name>")
# def user(name):
#     return f"Hello {name}!"

@app.route("/admin/")
def admin():
    return redirect(url_for("user", name="jim bob")) # name here references the value in < > during the @app.route() line

@app.route("/about/")
def aboutPage():
    return render_template("about.html")


@app.route("/login/", methods=["POST", "GET"])
def login():
    session.permanent = True
    if request.method == "POST":
        varUser = request.form["nm"]
        session["user"] = varUser
        flash(f"Login successful! Welcome, {varUser}!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/user/", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash("Email was saved!")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", email=email)
    else:
        flash("You are not currently logged in.")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"{user} has been successfully logged out.", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)