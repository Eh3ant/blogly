from flask import Flask, render_template, redirect, request,flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post,PostTag,Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "ehsan"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home_page():
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('home.html', posts=recent_posts)

@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('list.html', users=users)

@app.route('/users/new', methods=["GET", "POST"])
def add_new_user():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        image_url = request.form.get("image_url") 

        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

        db.session.add(new_user)
        db.session.commit()
        
        flash('User successfully created!', 'success')
        return redirect('/users')
    return render_template('add-user.html')

@app.route('/users/<int:user_id>', methods=['GET','POST'])
def show_user(user_id):
    found_user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        new_post = Post(title=title, content=content, user_id=user_id)

        db.session.add(new_post)
        db.session.commit()
        return redirect(f'/users/{user_id}')
    return render_template('user-details.html', user=found_user, posts=found_user.posts)

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

    flash('User and their posts have been successfully deleted!', 'success')
    return redirect('/users')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = post.user
    tags = post.tags
    return render_template('post-details.html', post=post,user=user,tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['GET', 'POST'])
def add_post(user_id):
    tags = Tag.query.all()
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        selected_tags = request.form.getlist('tags')

        new_post = Post(title=title, content=content, user_id=user_id)

        for tag_id in selected_tags:
            tag = Tag.query.get(tag_id)
            new_post.tags.append(tag)

        db.session.add(new_post)
        db.session.commit()
        
        flash('Post successfully created!', 'success')
        return redirect(f'/users/{user_id}')
    return render_template('add-post.html', user=user,tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']

        post.tags.clear()

        tag_ids = request.form.getlist('tags')
        for tag_id in tag_ids:
            tag = Tag.query.get(tag_id)
            post.tags.append(tag)

        db.session.commit()

        flash('Post successfully updated!', 'success')
        return redirect(f'/posts/{post_id}')
    return render_template('edit-post.html', post=post,tags=tags)

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template('tags.html',tags=tags) 


@app.route('/tag/new',methods=['GET','POST'])
def create_tag():
    if request.method == 'POST':

        tag_name = request.form['tag']

        new_tag = Tag(name=tag_name)

        db.session.add(new_tag)
        db.session.commit()

        flash('Tag created successfully!', 'success')
        return redirect('/tags')
    

    return render_template('create_tag.html')

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template('tag-details.html', tag=tag,posts=posts)


@app.route('/tags/<int:tag_id>/edit',methods=['GET', 'POST'])
def edit_tag(tag_id):
    found_tag = Tag.query.get_or_404(tag_id)

    if request.method == 'POST':
        found_tag.name = request.form['tag']
        db.session.commit()
        return redirect(f'/tags')
    
    return render_template('edit-tag.html', tag=found_tag)


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')






  



    






    



