from flask import Flask, render_template, session, flash, request, redirect, url_for
from datetime import timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "HouseFood"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=1)

db = SQLAlchemy(app)


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String)
    
    def __init__(self, email, password):
        self.email = email
        self.password = password
    

#GLOBAL VARIABLES
####isLoggedIn = False

@app.route("/")
def start():
    isLoggedIn = False
    #check if logged in
    if "user" in session:
        user = session["user"]
        isLoggedIn = True
        userId = users.query.filter_by(email=user).first().id
    if not isLoggedIn:
        return redirect(url_for("home", userId="home", isLoggedIn=isLoggedIn))
    else:
        return redirect(url_for("home", userId=userId, isLoggedIn=isLoggedIn))


@app.route("/<userId>", methods=['GET', 'POST'])
def home(userId):
    isLoggedIn = False 
    #check if logged in
    if "user" in session:
        user = session["user"]
        isLoggedIn = True
        userId = users.query.filter_by(email=user).first().id
    
    if request.method == 'GET':
        #by each next or previous load appropriate cards from db
        ###
    
        #get cards from db
        ###
    
        #send cards to frontend
        ###
        if not isLoggedIn:
            return render_template("home.html", userId="home", isLoggedIn=isLoggedIn)
        else:
            return render_template("home.html", userId=userId, isLoggedIn=isLoggedIn)
    
    else:
        chefId = request.form['chefId']
        mealId = request.form['mealId']
        if chefId:
            return redirect(url_for("profile", chefId))
        elif mealId:
            return redirect(url_for("profile", mealId))


@app.route("/register", methods=['POST', 'GET'])
def register():
    #if i am posting
    if request.method == 'POST':
        #grab data from forms
        registerEmail = request.form['registerEmail']
        registerPassword = request.form['registerPassword']
        registerConfirm = request.form['registerConfirm']
        
        #check if input is missing
        if not registerEmail:
            flash("Email Is Required", "info")
            return redirect(url_for('register'))
        if not registerPassword:
            flash("Email Is Required", "info")
            return redirect(url_for('register'))
        if registerPassword != registerConfirm:
            flash("Passwords Don't Match Is Required", "info")
            return redirect(url_for('register'))
        
        #hash the password
        hashedRegisterPassword = generate_password_hash(registerPassword)
        
        #check if email exists
        foundUser = users.query.filter_by(email=registerEmail).first()
        if foundUser:
            #if email already exists
            flash("Email Already Exists, Log In!", "info")
            return redirect(url_for('login'))
        else:
            #add to db
            user = users(registerEmail, hashedRegisterPassword)
            db.session.add(user)
            db.session.commit()
            # Forget any user email
            session.clear()
            #add to sessions
            session.permanent = True
            session['user'] = registerEmail
            isLoggedIn = True
            #grab user id
            userId = users.query.filter_by(email=registerEmail).first().id
            #render home page with input of user id and is logged in
            return redirect(url_for("home", userId=userId, isLoggedIn=isLoggedIn))    
    else:
        isLoggedIn = False
        if "user" in session:
            isLoggedIn = True
            #grab user id
            userId = users.query.filter_by(email=session['user']).first().id
            return redirect(url_for("home", userId=userId, isLoggedIn=isLoggedIn))
        return render_template("register.html")
    
    
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        loginEmail = request.form['loginEmail']
        loginPassword = request.form['loginPassword']
        
        #check if user typed email and password
        if not loginEmail:
            flash("Email Is Required", "info")
            return redirect(url_for(login))
        if not loginPassword:
            flash("Password Is Required", "info")
            return redirect(url_for("login"))
        
        #check if username exists
        foundUser = users.query.filter_by(email=loginEmail).first()
        if not foundUser:
            flash("Username Doesn't Exist", "info")
            return redirect(url_for("login"))
        
        #get the password of this user name from Db
        userPassword = users.query.filter_by(email=loginEmail).first().password  
        #check hash password
        if not check_password_hash(userPassword, loginPassword):
            flash("Password Is Not Correct", "info")
            return redirect(url_for("login"))
        
        # Forget any user email
        session.clear()
        #add to sessions
        session.permanent = True
        session['user'] = loginEmail
        isLoggedIn = True 
        
        #get user Id
        userId = users.query.filter_by(email=loginEmail).first().id
        
        return redirect(url_for("home", userId=userId, isLoggedIn=isLoggedIn))
    else:
        isLoggedIn = False
        if "user" in session:
            isLoggedIn = True
            #grab user id
            userId = users.query.filter_by(email=session['user']).first().id
            return redirect(url_for("home", userId=userId, isLoggedIn=isLoggedIn))
        return render_template("login.html")
  
    
@app.route("/logout")
def logout():
    #clear session
    session.clear()
    flash("You Are Logged Out!", "info")
    return redirect(url_for("login"))

@app.route("/subscribe", methods=['POST'])
def subscribe():
    subscribeEmail = request.form['subscribeEmail']
    
    #add email to db
    ###
    
    #send confirmation email
    ###
    
    return redirect(url_for("home", userId="home", isLoggedIn=isLoggedIn))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/cart")
def cart():
    #check if logged in
    if "user" in session:
        user = session["user"]
        isLoggedIn = True
        
        #get the cards of this user from db
        ###
        
        #render cart
        ###
        
    #redirect to login
    return render_template("cart.html")


@app.route("/profile")
def profile():
    isMine = False
    if "user" in session:
        user = session["user"]
        isLoggedIn = True
        
        if user == profileId:
            isMine = True
        
    #redirect to login
    return render_template("profile.html")


@app.route("/editProfile")
def editProfile():
    return render_template("editProfile.html")


@app.route("/meal")
def meal(mealId):
    if "user" in session:
        user = session["user"]
        isLoggedIn = True
        
        
@app.route("/addMeal")
def addMeal(userId):
    return render_template("addMeal.html")
        
    #redirect to login
    return render_template("meal.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)