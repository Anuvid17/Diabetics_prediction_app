from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
from flask_bcrypt import Bcrypt

'''a route refers to the URL pattern that a web application
responds to.  
It matches with the requested URL to the route and calls the associated
function to generate a response.'''

bcrypt = Bcrypt(app)
app.config["SECRET_KEY"] = "thisissecuritykey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

# "mysql+pymysql://root:Bca_2022@localhost:3306/user_details"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from healthcare import routes