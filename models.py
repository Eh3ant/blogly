
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

    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} user_id={p.user_id}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String,
                      nullable=False)
    
    content = db.Column(db.String,
                        nullable=False)
    
    created_at = db.Column(db.DateTime,nullable=False,default=db.func.now())

    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    tags = db.relationship('Tag',secondary="post_tag",backref="posts")


class Tag(db.Model):
    __tablename__ = 'tags'

    def __repr__(self):
        t = self
        return f"<Tag id={t.id} name={t.name}>"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

    name = db.Column(db.Text,nullable=False,unique=True)



class PostTag(db.Model):
    __tablename__ = "post_tag"

    post_id = db.Column(db.Integer,db.ForeignKey("posts.id"),nullable=False,primary_key=True)  

    tag_id = db.Column(db.Integer,db.ForeignKey("tags.id"),nullable=False,primary_key=True)      

    
                                                  