from flask import Blueprint, render_template, session, flash, redirect, url_for, request
from flask_login import current_user
from api.book_api import BookClient
from api.order_api import OrderClient
import requests, forms
from api.user_api import UserClient
frontend_blueprint = Blueprint('frontend', __name__)


@frontend_blueprint.context_processor
def cart_count():
    count = 0
    order = session.get('order')

    if order:
        for item in order.get('order_items'):
            count += item['quantity']

    return {'cart_items': count}


@frontend_blueprint.route('/', methods = ["GET"])
def home():
    if current_user.is_authenticated:
        session['order'] = OrderClient.get_order_from_session()

    try:
        books = BookClient.get_books()
    except:
        books = {
            "result": []
        }

    return render_template('index.html', books=books)


@frontend_blueprint.route('/register', methods=['POST', 'GET'])
def register_user():
    # Converting forms to custom defined forms that are created in forms.py
    form = forms.RegistrationForm(request.form)
    if request.method == "POST":
        # Checks if values are valid on submit
        if form.validate_on_submit():
            username = form.username.data

            if UserClient.user_exists(username):
                flash("Please try another user name")
                return render_template('register.html', form=form)
            else:
                user = UserClient.create_user(form)
                if user:
                    flash("User has been registered. Please login")
                    return redirect(url_for('frontend.home'))
        else:
            flash("Errors")

    return render_template('register.html', form=form)


@frontend_blueprint.route('/login', methods=["POST", "GET"])
def user_login():
    form = forms.LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            api_key, user = UserClient.login_user(form)
            # Store api_key in session if it's found
            if api_key:
                session['user_api_key'] = api_key
                temp_user = UserClient.get_user()
                if temp_user:
                    user = temp_user
                session['user'] = user

                # Getting logged-in user's open order and saving it in session
                order = OrderClient.get_order()
                if order.get('result'):
                    session['order'] = order['result']

                flash("Welcome back!")
                return redirect(url_for("frontend.home"))
            else:
                flash("Cannot login")
        else:
            flash("Cannot login")

    return render_template("login.html", form=form)


@frontend_blueprint.route('/logout', methods=["GET"])
def user_logout():
    session.clear()
    flash("User logged out")
    return redirect(url_for("frontend.home"))


@frontend_blueprint.route('/book/<slug>', methods=["GET", "POST"])
def book_details(slug):
    response = BookClient.get_book(slug)
    book = response['result']

    form = forms.ItemForm(book_id=book['id'])

    if request.method == "POST":
        # Checking if user is logged in
        if 'user' not in session:
            flash("Please Login")
            return redirect(url_for('frontend.user_login'))

        # Moving forward if user is logged in
        order = OrderClient.add_to_cart(book_id=book['id'], quantity=1)
        session['order'] = order['result']
        flash("Book added to cart")

    return render_template("book_info.html", book=book, form=form)


@frontend_blueprint.route('/checkout', methods=["GET"])
def checkout():
    # Checking if user is logged in
    if 'user' not in session:
        flash("Please Login")
        return redirect(url_for('frontend.user_login'))

    # Checking if user has entered any item in cart
    if 'order' not in session:
        flash("Please add some items to the cart first")
        return redirect(url_for('frontend.home'))

    order = OrderClient.get_order()

    # Making sure that user has at least 1 item in the cart
    if len(order['result']['order_items']) == 0:
        flash("Please add some items to the cart first")
        return redirect(url_for('frontend.home'))

    OrderClient.checkout()

    return redirect(url_for("frontend.thank_you"))


@frontend_blueprint.route('/thank-you', methods=["GET"])
def thank_you():
    # Checking if user is logged in
    if 'user' not in session:
        flash("Please Login")
        return redirect(url_for('frontend.user_login'))

    # Checking if user has entered any item in cart
    if 'order' not in session:
        flash("Please add some items to the cart first")
        return redirect(url_for('frontend.home'))

    session.pop('order', None)
    flash("Your order is processing")

    return render_template('thankyou.html')

