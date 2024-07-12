from flask import Flask, redirect, url_for, render_template
import requests
import json

app = Flask(__name__)

# what is returned when url "/home" is navigated
@app.route("/")
def home():
    return render_template("index.html")

# when url "/home/" is navigated to, redirects user to actual "home" function
@app.route("/home/")
def direct_home():
    return redirect(url_for("home")) # with option to specify argument , param=""

# says hello to whatever url is navigated to
@app.route("/<name>")
def user(name):
    return f"Hello {name}!"

@app.route("/admin/")
def admin():
    return redirect(url_for("user", name="jim bob")) # name here references the value in < > during the @app.route() line

@app.route("/about/")
def aboutPage():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)