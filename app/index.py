from flask import render_template
from flask_login import current_user
import datetime

from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.user import User

from .models.product import Product
from .models.purchase import Purchase
from .models.user import User
from .models.review import Review
from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all(True)
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases)
    

@bp.route('/mycart')
def mycart():
    cart = Cart.get_all_by_uid(current_user.id)
    if current_user.is_authenticated:
        cart = Cart.get_all_by_uid(current_user.id)
    else:
        cart = Nones
    # render the page by adding information to the index.html file
    return render_template('mycart.html', cart = cart)

@bp.route('/myaccount')
def myaccount():
    # find the products current user has bought:
    if current_user.is_authenticated:
        user = User.get(current_user.id)
        reviews = Review.get_all_by_uid(current_user.id)
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        return render_template('myaccount.html', user = user,
                           purchase_history=purchases, review_history=reviews)
    else:
        return redirect(url_for('users.login'))
    # render the page by adding information to the index.html file



'''
@bp.route('/myorders')
def myorders():
    # find the products current user has previously ordered:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the myorders.html file
    return render_template('myorders.html',
                           purchases=purchases)
'''