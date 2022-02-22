from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date


## Delete this code:
# import requests
# posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    posts = db.session.query(BlogPost).all()
    db.session.commit()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    requested_post = None
    # for blog_post in posts:
    #     print(blog_post)
    #     print(index)
    #     if blog_post["id"] == index:
    #         requested_post = blog_post
    #     print(requested_post)
    requested_post = BlogPost.query.get(post_id)
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/edit_post/<int:post_id>", methods=['GET', 'POST', 'PATCH'])
def edit_post(post_id):
    heading = "Edit Post"
    current_post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=current_post.title,
        subtitle=current_post.subtitle,
        author=current_post.author,
        img_url=current_post.img_url,
        body=current_post.body
    )
    if edit_form.validate_on_submit():
        current_post.title = edit_form.title.data
        current_post.subtitle = edit_form.subtitle.data
        current_post.author = edit_form.author.data
        current_post.img_url = edit_form.img_url.data
        current_post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for('show_post', post_id=current_post.id))
    return render_template("make-post.html", form=edit_form, heading=heading)


@app.route("/new_post", methods=['GET', 'POST'])
def new_post():
    heading = "New Post"
    form = CreatePostForm()
    if form.validate_on_submit():
        new_article = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            date=date.today().strftime("%B %d, %Y"),
            body=form.body.data,
            author=form.author.data,
            img_url=form.img_url.data )
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template("make-post.html", form=form, heading=heading)

@app.route("/delete/<int:post_id>")
def delete(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    print("deletujemy")
    return redirect(url_for('get_all_posts'))

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
