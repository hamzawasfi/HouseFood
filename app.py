import sqlalchemy_utils
from flask_mail import Mail, Message
from flask import Flask, render_template, session, flash, request, redirect, url_for
from datetime import timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from werkzeug.utils import secure_filename
import os
import datetime

app = Flask(__name__)
app.secret_key = "HouseFood"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hamzawasfi58@gmail.com'
app.config['MAIL_PASSWORD'] = 'qxfc xfiu ufcz uogi'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['UPLOAD_FOLDER'] = 'static/photos'
app.permanent_session_lifetime = timedelta(days=1)

db = SQLAlchemy(app)
mail = Mail(app)


#DATABASE MODELS
class subscribed(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100))
    
    def __init__(self, email):
        self.email = email


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String, nullable=False)
    
    def __init__(self, email, password):
        self.email = email
        self.password = password

        
class persons(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey(users.id))
    name = db.Column(db.String(100), nullable=True)
    photo = db.Column(sqlalchemy_utils.types.url.URLType(), nullable=True)
    intro = db.Column(db.String(), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    earned = db.Column(db.Integer, nullable=True)
    isMine = False
    reviewCount = 0
    reviewAvg = 0
    topMeal = None
    
    def __init__(self, userId, name, photo, intro, location, earned):
        self.userId = userId
        self.name = name
        self.photo = photo
        self.intro = intro
        self.location = location
        self.earned = earned
        
    def addIsMine(self, isMine):
        self.isMine = isMine
        
    def addReviewCount(self, reviewCount):
        self.reviewCount = reviewCount
        
    def addReviewAvg(self, reviewAvg):
        self.reviewAvg = reviewAvg
        
    def addTopMeal(self, topMeal):
        self.topMeal = topMeal
        
        
class notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    personId = db.Column(db.Integer, db.ForeignKey(persons.id), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __init__(self, personId, type):
        self.personId = personId
        self.type = type


class purchases(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    notificationId = db.Column(db.Integer, db.ForeignKey(persons.id), nullable=False)
    fromId = db.Column(db.Integer, db.ForeignKey(persons.id), nullable=False)
    mealId = db.Column(db.Integer, db.ForeignKey(persons.id), nullable=False)
    earned = db.Column(db.Integer, nullable=False)
    
    def __init__(self, notificationId, fromId, mealId, earned):
        self.notificationId = notificationId
        self.fromId = fromId
        self.mealId = mealId
        self.earned = earned
      
      
class requests(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    notificationId = db.Column(db.Integer, db.ForeignKey(persons.id), nullable=False)
    fromId = db.Column(db.Integer, db.ForeignKey(persons.id), nullable=False)
    text = db.Column(db.String(), nullable=True)
    
    def __init__(self, notificationId, fromId, text):
        self.notificationId = notificationId
        self.fromId = fromId
        self.text = text
    
    
    
class chefs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    personId = db.Column(db.Integer, db.ForeignKey(persons.id), nullable=False)
    topMeal = object
    
    def __init__(self, personId):
        self.personId = personId
        
    def addTopMeal(self, topMeal):
        self.topMeal = topMeal
    

class meals(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chefId = db.Column(db.Integer, db.ForeignKey(chefs.id), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(), nullable=True)
    price = db.Column(db.Integer, nullable=False)
    person = dict()
    photos = list()
    ingridients = list()
    total = 0
    reviewCount = 0
    reviewAvg = 0
    
    def __init__(self, chefId, name, intro, price):
        self.chefId = chefId
        self.name = name
        self.intro = intro
        self.price = price
        
    def addPerson(self, personId, ChefName):
        self.person = {'id': personId, 'name': ChefName}
        
    def addPhotos(self, photos):
        self.photos = photos
    
    def addIngridients(self, ingridients):
        self.ingridients = ingridients
        
    def addTotal(self, total):
        self.total = total
        
    def addReviewCount(self, reviewCount):
        self.reviewCount = reviewCount
        
    def addReviewAvg(self, reviewAvg):
        self.reviewAvg = reviewAvg
        

class meal_photos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mealId = db.Column(db.Integer, db.ForeignKey(meals.id), nullable=False)
    photo = db.Column(db.String(), nullable=True)
    
    def __init__(self, mealId, photo):
        self.mealId = mealId
        self.photo = photo


class ings(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mealId = db.Column(db.Integer, db.ForeignKey(meals.id), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    def __init__(self, mealId, name):
        self.mealId = mealId
        self.name = name
        
        
class reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mealId = db.Column(db.Integer, db.ForeignKey(meals.id), nullable=False)
    personId = db.Column(db.Integer, db.ForeignKey(persons.id), nullable=False)
    text = db.Column(db.String(), nullable=False)
    review = db.Column(db.Integer, nullable=False)
    person = str
    meal = str
    
    def __init__(self, mealId, personId, text, review):
        self.mealId = mealId
        self.personId = personId
        self.text = text
        self.review = review
        
    def addPerson(self, person):
        self.person = person
        
    def addMeal(self, meal):
        self.meal = meal
        
        
class carts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mealId = db.Column(db.Integer, db.ForeignKey(meals.id), nullable=False)
    personId = db.Column(db.Integer, db.ForeignKey(persons.id), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    meal = meals
    
    def __init__(self, mealId, personId, amount):
        self.mealId = mealId
        self.personId = personId
        self.amount = amount
    
    def addMeal(self, meal):
        self.meal = meal
        
with app.app_context():
    #db.drop_all()
    db.create_all()
app.run(debug=True)
          
#APP ROUTES
@app.route("/", methods=['GET', 'POST'])
def home():
    session["isLoggedIn"] = False
    #check if logged in
    if "user" in session:
        user = session["user"]
        session['isLoggedIn'] = True
        user = users.query.filter_by(email=user).first()
        person = persons.query.filter_by(userId=user.id).first()
    
        if request.method == 'GET':
        
            #get meals from db
            foundMeals = meals.query.all()
            
            #get meal photos ,chef
            for foundMeal in foundMeals:
                #person
                foundMealChefId = chefs.query.filter_by(id=foundMeal.chefId).first().id
                foundMealPerson = persons.query.filter_by(id=foundMealChefId).first()   
                foundMeal.addPerson(foundMealPerson.id, foundMealPerson.name)
                
                #photos
                foundMealPhotos = meal_photos.query.filter_by(mealId=foundMeal.id).all()
                foundPhotos = list()
                for foundMealPhoto in foundMealPhotos:
                    foundPhotos.append(foundMealPhoto.photo)
                foundMeal.addPhotos(foundPhotos)
                
                #reviews
                foundMealReviews = reviews.query.filter_by(mealId=foundMeal.id).all()
                if foundMealReviews:
                    foundMeal.addReviewCount(len(foundMealReviews))
                    avgReviews = 0
                    for foundMealReview in foundMealReviews:
                        avgReviews += foundMealReview.review
                    avgReviews /= len(foundMealReviews)
                    foundMeal.addReviewAvg(int(avgReviews))
                
            
            #get persons these are chefs 
            foundChefs = chefs.query.all()
            foundPersons = []
            for foundChef in foundChefs:
                chefPerson = persons.query.filter_by(id=foundChef.personId).first()
                foundPersons.append(chefPerson)

                topReview = -1
                topMeal = meals
                chefReviews = reviews.query.filter_by(personId=chefPerson.id).all()
                for chefReview in chefReviews:
                    if chefReview.review > topReview:
                        topReview = chefReview.review
                        topMeal = meals.query.filter_by(id=chefReview.mealId).first()
                        
                foundChef.addTopMeal(topMeal)
                    
            #reviews
            if foundChefs:
                foundChefReviews = reviews.query.filter_by(personId = foundChef.personId).all()
                if foundChefReviews:
                    for foundPerson in foundPersons:
                        foundPerson.addReviewCount(len(foundChefReviews))                
                        avgReviews = 0
                        topMeal = None
                        for foundChefReview in foundChefReviews:
                            avgReviews += foundChefReview.review
                            
                            if foundChefReviews.index(foundChefReview) == 0:
                                topMeal = foundChefReview.mealId
                            elif foundChefReview.review > foundChefReviews[foundChefReviews.index(foundChefReview) - 1].review:
                                topMeal = foundChefReview.mealId
                        foundPerson.addTopMeal(meals.query.filter_by(id=topMeal).first())       
                        avgReviews /= len(foundChefReviews)
                        foundPerson.addReviewAvg(int(avgReviews))        
            
            #notifications
            notis = notifications.query.filter_by(personId=user.id).all()
            notisLength = 0
            if notis:
                notisLength = len(notis)
            
            total = 0
            cartItems = carts.query.filter_by(personId=user.id).all()    
            if cartItems:
                for item in cartItems:
                    meal = meals.query.filter_by(id=item.mealId).first()
                    #photos
                    foundMealPhotos = meal_photos.query.filter_by(mealId=meal.id)
                    foundPhotos = list()
                    for foundMealPhoto in foundMealPhotos:
                        foundPhotos.append(foundMealPhoto.photo)
                    meal.addPhotos(foundPhotos)
                            
                    mealTotal = float(meal.price) * float(item.amount)
                    total += mealTotal
                    meal.addTotal(mealTotal)
            session["total"] = total
            return render_template("home.html", person=person, total=total, notificationCount=notisLength, notifications=notis, isLoggedIn=session['isLoggedIn'], persons=foundPersons, meals=foundMeals)
        
        else:
            #get values from the form.
            profileId = request.form['profileId']
            mealId = request.form['mealId']
            type = request.form['homeCardType']
            amount = 1

            try:
                amount = request.form['mealMealAmount']
            except:
                pass
            
            try:
                topMeal = request.form['chefTopMeal']
            except:
                pass
            
            
            if type == 'Chef':
                homeSubmitChef = request.form['homeSubmittedChef']
                print(homeSubmitChef)
                if homeSubmitChef == "homeChefMeal":
                    meal = meals.query.filter_by(id=topMeal).first()
                    return redirect(url_for("meal", mealId=meal.id))
                elif homeSubmitChef == "homeChefChef":
                    profile = persons.query.filter_by(id=profileId).first()
                    return redirect(url_for("profile", profileId=profile.id))
            elif type == 'Meal':
                homeSubmitMeal = request.form['homeSubmittedMeal']
                if homeSubmitMeal == "homeMealMeal":
                    meal = meals.query.filter_by(id=mealId).first()
                    return redirect(url_for("meal", mealId=meal.id))
                elif homeSubmitMeal == "homeMealChef":
                    profile = persons.query.filter_by(id=profileId).first()
                    return redirect(url_for("profile", profileId=profile.id))
                elif homeSubmitMeal == "homeMealOrder":
                    cart = carts.query.filter_by(mealId=mealId, personId=person.id).first()
                    if cart:
                        cart.amount += amount
                        db.session.commit()
                    else:
                        cart = carts(mealId, person.id, amount)
                        db.session.add(cart)
                        db.session.commit()
                    return redirect(url_for("home"))
            return redirect(url_for("home"))
    else:
        person = {'id':'home', 'name':'Name'}
        total = 0
                
        return render_template("home.html", person=person, total=total, notificationCount=notisLength, notifications=notis, isLoggedIn=session['isLoggedIn'], persons=None, meals=None)

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
            #add to db users
            user = users(registerEmail, hashedRegisterPassword)
            db.session.add(user)
            db.session.commit()
                        
            #add to db persons
            person = persons(user.id, "Name", "placeholder.jpg", "Brief about you", "Your location", 0)
            db.session.add(person)
            db.session.commit()
            
            session.clear()
            
            #add to sessions
            session.permanent = True
            session['user'] = registerEmail
            session['isLoggedIn'] = True
            
            #render home page with input of user id and is logged in
            return redirect(url_for("home"))    
    else:
        if "user" in session:
            session['isLoggedIn'] = True
                        
            return redirect(url_for("home"))
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
        session['isLoggedIn'] = True
                
        return redirect(url_for("home"))
    else:
        if "user" in session:
            session['isLoggedIn'] = True
                        
            return redirect(url_for("home"))
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
    subscriber = subscribed(subscribeEmail)
    db.session.add(subscriber)
    db.session.commit()
    
    #send confirmation email
    message = Message("Subscribed To HouseFood", sender='noreply@housefood.com', recipients=[subscribeEmail])
    message.body = "Thank you for subscribing to HouseFood!"
    mail.send(message)
        
    return redirect(url_for("home"))


@app.route("/about")
def about():
    session["isLoggedIn"] = False
    total = 0
    #check if logged in
    if "user" in session:
        user = session["user"]
        total = session["total"]
        session["isLoggedIn"] = True
        user = users.query.filter_by(email=user).first()
        person = persons.query.filter_by(userId=user.id).first()
        
        #notifications
        notis = notifications.query.filter_by(personId=user.id).all()
        notisLength = 0
        if notis:
            notisLength = len(notis)
        
        return render_template("about.html", person=person, total=total, notifications=notis, notificationCount=notisLength, isLoggedIn=session["isLoggedIn"])
    return render_template("about.html", person=None, total=0, isLoggedIn=session["isLoggedIn"])


@app.route("/cart/<personId>")
def cart(personId):
    #check if logged in
    session["isLoggedIn"] = False
    if "user" in session:
        user = session["user"]
        session["isLoggedIn"] = True
        user = users.query.filter_by(email=user).first()
        person = persons.query.filter_by(userId=user.id).first()
        notis = notifications.query.filter_by(personId=user.id).all()
        notisLength = 0
        if notis:
            notisLength = len(notis)
        total = 0
        
        if request.method == 'GET':
            cartItems = carts.query.filter_by(personId=user.id).all()
            if cartItems:
                for item in cartItems:
                    meal = meals.query.filter_by(id=item.mealId).first()
                    #photos
                    foundMealPhotos = meal_photos.query.filter_by(mealId=meal.id)
                    foundPhotos = list()
                    for foundMealPhoto in foundMealPhotos:
                        foundPhotos.append(foundMealPhoto.photo)
                    meal.addPhotos(foundPhotos)
                        
                    mealTotal = float(meal.price) * float(item.amount)
                    total += mealTotal
                    meal.addTotal(mealTotal)
                    item.addMeal(meal)
        if request.method == 'POST':
            total = request.form['cartPurchase']
            
            #send email to seller
            cartItems = carts.query.filter_by(personId=user.id).all()
            if cartItems:
                for item in cartItems:
                    meal = meals.query.filter_by(id=item.mealId).first()
                    seller = chefs.query.filter_by(id=meal.chefId).first()
                    
                    mealTotal = int(meal.price) * int(item.amount)
                    
                    sellerEmail = seller.email
                    message = Message(f"Succesfull Sell at HouseFood", sender='noreply@housefood.com', recipients=[sellerEmail])
                    message.body = "You have earned ${mealTotal} from selling {meal.name} from {person.name}, {item.amount} times, congratulations!"
                    mail.send(message)
                    
                    #add earned to seller
                    seller.earned += mealTotal
                    
                    #send notification to seller
                    notification = notifications(seller.id, "purchase")
                    db.session.add(notification)
                    db.session.commit()
                    
                    purchase = purchases(notification.id, user.id, meal.id, mealTotal)
                    db.session.add(purchase)
                    db.session.commit()
                                
            #send email to buyer
            buyerEmail = user.email
            message = Message(f"Succesfull purchase at HouseFood", sender='noreply@housefood.com', recipients=[buyerEmail])
            message.body = "You have paid ${total} at HouseFood, Thanks!"
            mail.send(message)
            
            return redirect(url_for("cart", person.id))

        return render_template("cart.html", person=person, total=total, notifications=notis, notificationCount=notisLength, isLoggedIn=session["isLoggedIn"], cards=cartItems)
    else:
        return redirect(url_for("login"))
            


@app.route("/profile/<profileId>", methods=['POST', 'GET'])
def profile(profileId):
    session['isLoggedIn'] = False
    total = 0
    if "user" in session:
        session['isLoggedIn'] = True
        total = session["total"]
        user = users.query.filter_by(email=session['user']).first()
        person =  persons.query.filter_by(userId=user.id).first() 
        profile = persons.query.filter_by(userId=profileId).first()
        chef = chefs.query.filter_by(personId=profileId).first()
        notis = notifications.query.filter_by(personId=user.id).all()
        notisLength = 0
        if notis:
            notisLength = len(notis)
        profile.addIsMine(False)
        if int(user.id) == int(profile.id):
            profile.addIsMine(True)
        
        if request.method =="GET":
            if chef:
                meal = meals.query.filter_by(chefId=chef.id).all()
                review = reviews.query.filter_by(personId=profileId).all()
                
                #get meal photos ,chef
                for foundMeal in meal:
                    #photos
                    foundMealPhotos = meal_photos.query.filter_by(mealId=foundMeal.id)
                    foundPhotos = list()
                    for foundMealPhoto in foundMealPhotos:
                        foundPhotos.append(foundMealPhoto.photo)
                    foundMeal.addPhotos(foundPhotos)
                    
                    #reviews
                    foundMealReviews = reviews.query.filter_by(mealId=foundMeal.id).all()
                    if foundMealReviews:
                        foundMeal.addReviewCount(len(foundMealReviews))
                        avgReviews = 0
                        for foundMealReview in foundMealReviews:
                            avgReviews += foundMealReview.review
                        avgReviews /= len(foundMealReviews)
                        foundMeal.addReviewAvg(int(avgReviews))
                
                foundChefReviews = reviews.query.filter_by(personId = profile.id).all()
                if foundChefReviews:
                    profile.addReviewCount(len(foundChefReviews))                
                    avgReviews = 0
                    for foundChefReview in foundChefReviews:
                        avgReviews += foundChefReview.review
                    avgReviews /= len(foundChefReviews)
                    profile.addReviewAvg(int(avgReviews))
                
                #get the reviews
                for foundReview in review:
                    foundReviewMeal = meals.query.filter_by(id=foundReview.mealId).first().name
                    
                    foundReview.addPerson(person.name)
                    foundReview.addMeal(foundReviewMeal)
                
                return render_template("profile.html", person=person, total=total, notifications=notis, notificationCount=notisLength, isLoggedIn=session['isLoggedIn'], profile=profile, meals=meal, reviews=review)    
            else:
                return render_template("profile.html", person=person, total=total, notifications=notis, notificationCount=notisLength, isLoggedIn=session['isLoggedIn'], profile=profile)
        else:
            mealId = request.form['reviewMealId']
            personId = request.form['reviewPersonId']
            text = request.form['reviewText']
            rating = request.form['reviewRating']
            
            review = reviews(mealId, personId, text, rating)
            db.session.add(review)
            db.session.commit()
            
            return redirect(url_for("profile", profileId=profile.id)) 
    else:
        #redirect to login
        return redirect(url_for("login"))


@app.route("/editProfile/<profileId>", methods=['POST', 'GET'])
def editProfile(profileId):
    if request.method == 'GET':
        session['isLoggedIn'] = False
        total = 0
        
        #check if logged in
        if "user" in session:
            session['isLoggedIn'] = True
            total = session["total"]
            user = session["user"]
            user = users.query.filter_by(email=user).first()
            person = persons.query.filter_by(id=user.id).first()
            profile = persons.query.filter_by(userId=profileId).first()
            notis = notifications.query.filter_by(personId=user.id).all()
            notisLength = 0
            if notis:
                notisLength = len(notis)
            
            #check if my profile
            if int(user.id) != int(profile.id):
                return redirect(url_for("profile", profileId=user.id))
                   
        else:
            return redirect(url_for("login"))
        
        return render_template("editProfile.html", person=person, profile=profile, total=total, notifications=notis, notificationCount=notisLength, isLoggedIn=session["isLoggedIn"])
    else:
        #grab inputs from form
        editProfilePhoto = request.files['editProfilePhoto']
        editProfileName = request.form['editProfileName']
        editProfileIntro = request.form['editProfileIntro']
        editProfileLocation = request.form['editProfileLocation']
        editProfileEmail = request.form['editProfileEmail']
        
        #grab existing user and person
        foundUser = users.query.filter_by(email=session['user']).first()
        foundPerson = persons.query.filter_by(userId=foundUser.id).first()
        
        #assign one by one
        if editProfilePhoto:
            editProfilePhoto.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(editProfilePhoto.filename)))
            foundPerson.photo = editProfilePhoto.filename
        if editProfileName:
            foundPerson.name = editProfileName
        if editProfileIntro:
            foundPerson.intro = editProfileIntro
        if editProfileLocation:
            foundPerson.location = editProfileLocation
        if editProfileEmail:
            foundUser.email = editProfileEmail
            session['user'] = editProfileEmail
            
        #commit to db
        db.session.commit()
         
        profile = persons.query.filter_by(userId=profileId).first()
        return redirect(url_for("profile", profileId=profile.id))
        

@app.route("/meal/<mealId>")
def meal(mealId):
    session['isLoggedIn'] = False
    total = 0
    if "user" in session:
        user = session["user"]
        session['isLoggedIn'] = True
        total = session["total"]
        notis = notifications.query.filter_by(personId=user.id).all()
        notisLength = 0
        if notis:
            notisLength = len(notis)
        
        #get user id
        user = users.query.filter_by(email=user).first()
        person = persons.query.filter_by(id=user.id).first()
        
        #get the found meal        
        foundMeal = meals.query.filter_by(id=mealId).first()
        
        #get found meal photos
        foundMealPhotos = meal_photos.query.filter_by(mealId=mealId).all()
        foundMeal.addPhotos(foundMealPhotos)
        
        #get found meal ingridients
        foundMealIngridients = ings.query.filter_by(mealId=mealId).all()
        foundMeal.addIngridients(foundMealIngridients)
        
        #get the chef person id
        foundChefPersonId = chefs.query.filter_by(id=foundMeal.chefId).first().id
        
        #get person
        foundPerson = persons.query.filter_by(id=foundChefPersonId).first()
        foundMeal.addPerson(foundPerson.id, foundPerson.name)
        
        #get reviews
        foundMealReviews = reviews.query.filter_by(mealId=foundMeal.id).all()
        foundMeal.addReviewCount(len(foundMealReviews))
        avgReviews = 0
        for foundMealReview in foundMealReviews:
            avgReviews += foundMealReview.review
        avgReviews /= len(foundMealReviews)
        foundMeal.addReviewAvg(int(avgReviews))
        
        return render_template("meal.html", person=person, total=total, notifications=notis, notificationCount=notisLength, isLoggedIn=["isLoggedIn"], meal=foundMeal)
    else:
        return redirect(url_for('login'))
        
        
@app.route("/addMeal/<userId>", methods=['POST', 'GET'])
def addMeal(userId):
    if request.method == 'GET':
        session['isLoggedIn'] = False
        total = 0
        
        #check if logged in
        if "user" in session:
            user = session["user"]
            session['isLoggedIn'] = True
            total = session["total"]
            notis = notifications.query.filter_by(personId=user.id).all()
            notisLength = 0
            if notis:
                notisLength = len(notis)
            
            #get user id
            user = users.query.filter_by(email=user).first()
            person = persons.query.filter_by(id=userId).first()
            
                    
            #if not adding meal to his own
            if int(user.id) != int(person.id):
                return redirect(url_for("profile", profileId=user.id))
            
            return render_template("addMeal.html", person=person, total=total, notifications=notis, notificationCount=notisLength, isLoggedIn=session["isLoggedIn"])
        else:
            return redirect(url_for("login"))
    else:
        if "user" in session:
            user = session["user"]
            session['isLoggedIn'] = True
            
            #get user id
            user = users.query.filter_by(email=user).first()
            person = persons.query.filter_by(id=userId).first()
            
        #add a chef if does not exist
        if not chefs.query.filter_by(personId=person.id).first():
            chef = chefs(person.id)
            db.session.add(chef)
            db.session.commit()
        
        #get chef id
        chefId = chefs.query.filter_by(personId=person.id).first().id
        
        #grab inputs from form
        addMealName = request.form['addMealName']
        addMealIntro = request.form['addMealIntro']
        addMealPrice = request.form['addMealPrice']
        
        addMealPhotos = request.files.getlist('addMealPhoto')
        addMealIngredients = request.form['addMealIngridientList'].split(',')
        
        #assign one by one
        if not addMealName:
            addMealName = "Meal Name"
        if not addMealIntro:
            addMealIntro = "Meal Description"
        if not addMealPrice:
            addMealPrice = 0
            
        #add to db 
        meal = meals(chefId, addMealName, addMealIntro, addMealPrice)
        db.session.add(meal)
        db.session.commit()
        
        #add meal photos  
        if addMealPhotos[0].filename:
            for addMealPhoto in addMealPhotos:
                addMealPhoto.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(addMealPhoto.filename)))
                addMealPhoto = addMealPhoto.filename
                
                #add to meal photos db
                mealPhoto = meal_photos(meal.id, addMealPhoto)
                db.session.add(mealPhoto)
                db.session.commit()
        else:
            mealPhoto = meal_photos(meal.id, "placeholder.jpg")
            db.session.add(mealPhoto)
            db.session.commit()
            
        
        #add meal ingredients 
        if addMealIngredients:
            for addMealIngridient in addMealIngredients:
                #add to ingridients db
                ingridient = ings(meal.id, addMealIngridient)
                db.session.add(ingridient)
                db.session.commit()
        else:
            ingridients = ings(meal.id, "ingridients")
            db.session.add(ingridients)
            db.session.commit()
                    
        return redirect(url_for("meal", mealId=meal.id))      
        

