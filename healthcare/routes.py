from flask import render_template, flash, redirect, url_for, request, session, make_response
from healthcare.forms import Registrationform, Loginform
from healthcare import app,db, bcrypt
from healthcare.models import User
import pickle
import numpy as np

model = pickle.load(open("model.pkl","rb"))

@app.route('/')
def home():
    return render_template("homepage.html")

@app.route('/registration', methods=["GET", "POST"])
def registration():
    with app.app_context():
     db.create_all()
    form = Registrationform()
    if form.validate_on_submit():
        hashed_pass= bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        # flash(f"Account created for {form.username.data}", "success")
        return redirect(url_for('login'))
    return render_template("registration.html", form = form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = Loginform()
    if form.validate_on_submit():
        db_user = User.query.filter_by(username=form.username.data).first()
        if db_user and bcrypt.check_password_hash(db_user.password, form.password.data):
            # flash("Logged in successfully", "success")
            session['user'] = db_user.id
            return redirect(url_for("prediction"))
        else:
            flash("Bad credentials", "error")
    return render_template("login.html", form = form) 

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/prediction', methods=["GET", "POST"])
def prediction():
    if "user" in session:
        user_id = session['user']
        db_user = User.query.get(user_id)
        username = db_user.username if db_user else "User"
        response = make_response(render_template('prediction.html', username=username))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return response
    else:
        return redirect(url_for('login'))

@app.route('/logout', methods=["GET"])
def logout():
    if 'user' in session:
        user_id = session['user']
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
        session.pop('user', None)
    return redirect(url_for('registration'))

@app.route('/result', methods=["GET", "POST"])
def result():
    a = request.form.get('pregnancy')
    b = request.form.get('glucose')
    c = request.form.get('bp')
    d = request.form.get('skinthickness')
    e = request.form.get('insulin')
    f = request.form.get('bmi')
    g = float(request.form.get('pedigreefunction'))
    h = request.form.get('age')

    userdata = (a,b,c,d,e,f,g,h)
    userarray = np.asarray(userdata)
    reshaped = userarray.reshape(1,-1)
    prediction = model.predict(reshaped)
    if prediction == 0:
        result = "Not a diaboetic person"
    else:
        result = "Diaboetic person"

    return render_template('result.html', answer = result)    
