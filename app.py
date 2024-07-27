from flask import Flask, render_template, request

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return render_template("profile.html")