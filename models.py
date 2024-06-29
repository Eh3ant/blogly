
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()

"""Models for Blogly."""


class User(db.Model):
    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"


    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(50),
                           nullable=False)

    last_name = db.Column(db.String,
                          nullable=False)

    image_url = db.Column(db.String,
                          nullable=True) 
    
    posts = db.relationship('Post', backref='user', cascade='all, delete-orphan')

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String,
                      nullable=False)
    
    content = db.Column(db.String,
                        nullable=False)
    
    created_at = db.Column(db.DateTime,nullable=False,default=db.func.now())

    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    
                                                  