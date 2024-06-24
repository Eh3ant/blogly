"""Blogly application."""

from flask import Flask , render_template ,redirect ,request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "ehsan"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
""" db.create_all() """

@app.route('/')
def home_page():
    return redirect ('/users')

@app.route('/users')
def list_user():
    """Shows list off all users in db"""
    users = User.query.all()
    return render_template('list.html' ,users=users)

""" @app.route('/add/new' , methods=["post"])
def add_new_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]

    new_user = User(first_name=first_name,last_name=last_name,image_url=img_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users') """

@app.route('/users/new', methods=["GET", "POST"])
def add_new_user():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        image_url = request.form.get("image_url") 

        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

        db.session.add(new_user)
        db.session.commit()

        return redirect('/users')
    return render_template('add-user.html')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """ Show details about a single user"""
    found_user = User.query.get_or_404(user_id)
    return render_template('user_details.html',user=found_user)


@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    found_user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        found_user.first_name = request.form['first_name']
        found_user.last_name = request.form['last_name']
        found_user.image_url = request.form.get('image_url')

        db.session.commit()
        return redirect('/users')

    return render_template('edit.html', user=found_user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    found_user = User.query.get_or_404(user_id)
    db.session.delete(found_user)
    db.session.commit()
    return redirect('/users')



    



