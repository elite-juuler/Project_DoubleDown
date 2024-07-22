from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "Mko09ijn"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.permanent_session_lifetime = timedelta(days=2)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    gender = db.Column(db.String)

    def __init__(self, name, email):
        self.name = name
        self.email = email


# what is returned when url "/home" is navigated
@app.route("/")
def home():
    return render_template("index.html")

# display all users in db
@app.route("/viewusers")
def viewusers():
    return render_template("viewusers.html", values=users.query.all())

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
        
        found_user = users.query.filter_by(name=varUser).first() 
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(varUser, "")
            db.session.add(usr)
            db.session.commit()

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
        varUser = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=varUser).first()
            found_user.email = email
            db.session.commit()

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
    with app.app_context():
        db.create_all()
    app.run(debug=True)