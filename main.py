from flask import Flask, render_template, url_for, flash, redirect, request, session, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
# from flask_migrate import Migrate
from webforms import Login, EditProfile, EditEventForm, Sign_up, PostForm
from werkzeug.utils import secure_filename
import uuid as uuid
import os
import smtplib
from flask_mail import Mail,Message
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DATABASSE.db'
    db.init_app(app)

    UPLOAD_FOLDER = 'static/images/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(20), nullable=False, unique=True)
        email = db.Column(db.String(90), nullable=False, unique=True)
        date_add = db.Column(db.DateTime, default=datetime.utcnow)
        password_hash = db.Column(db.String(128))
        profil_pic = db.Column(db.String(), nullable=True)
        # posts = db.relationship('Post', backref='author')

        @property
        def password(self):
            raise AttributeError('password is not a readable attribute')

        @password.setter
        def password(self, password):
            self.password_hash = generate_password_hash(password)

        def verify_password(self, password):
            return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

    class Posts(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(90))
        start = db.Column(db.DateTime, nullable=False)
        end = db.Column(db.DateTime, nullable=False)
        author = db.Column(db.Integer, db.ForeignKey(
            'user.id'))
        date_posted = db.Column(db.DateTime, default=datetime.utcnow)
        slug = db.Column(db.String(90))
        place = db.Column(db.String(90))
        image = db.Column(db.String(), nullable=True)
        # poster_id = db.Column(db.Integer, db.Freignkey('user.id'))

        def __repr__(self):
            return '<Post %r>' % self.title


    class SecureModelView(ModelView):
        def is_accessible(self):
            if current_user.is_authenticated == 'admin@admin.com' and check_password_hash == 'admin':
                session['admin_logged_in'] = True
                return redirect(url_for('admin.index'))
            else:
                return abort(403)


    # class SecureAdminIndexView(AdminIndexView):
    #     def is_accessible(self):
    #         return current_user.is_authenticated and session.get('admin_logged_in')

    admin = Admin(app)
    admin.add_view(SecureModelView(Posts, db.session))
    admin.add_view(SecureModelView(User, db.session))
    

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = Login()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                if check_password_hash(user.password_hash, form.password.data):
                    login_user(user)
                    flash("Login Succesfull!")
                    return redirect(url_for('dashboard'))
                else:
                    flash('Wrong Password - Try Again.... ')
            else:
                flash(" This User Dosen't Exist - Try Again.... ")
                email = request.form['email']
                password = request.form['password']
    
                if email == 'admin@admin.com' and check_password_hash == 'admin':
                    session['admin_logged_in'] = True
                    return redirect(url_for('admin.index'))
        return render_template('login.html', form=form)

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        username = None
        form = Sign_up()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None:
                hashed_pw = generate_password_hash(
                    form.password_hash.data, 'sha256')
                user = User(username=form.username.data,
                            email=form.email.data, password_hash=hashed_pw)
                db.session.add(user)
                db.session.commit()
            username = form.username.data
            form.username.data = ''
            form.email.data = ''
            form.password_hash.data = ''
            flash('user added successfully!')
            return redirect(url_for('login'))
        return render_template('signup.html', form=form, username=username)

    @app.route('/update/<int:id>', methods=['GET', 'POST'])
    @login_required
    def update(id):
        form = EditProfile()
        name_to_update = User.query.get_or_404(id)
        if request.method == "POST":
            name_to_update.username = request.form['username']
            name_to_update.email = request.form['email']
            if 'profil_pic' in request.files:
                file = request.files['profil_pic']
                if file.filename != '':
                    filename = secure_filename(file.filename)
                    pic_name = str(uuid.uuid1()) + '_' + filename
                    file.save(os.path.join(
                        app.config['UPLOAD_FOLDER'], pic_name))
                    name_to_update.profil_pic = pic_name
            try:
                db.session.commit()
                flash("User Was Updated Successfully!")
                return render_template('update.html',
                                       form=form,
                                       name_to_update=name_to_update,
                                       id=id)
            except:
                flash("Error! Looks like there was a problem. Please try again.")
                return render_template('update.html',
                                       form=form,
                                       name_to_update=name_to_update)

        return render_template('update.html',
                               form=form,
                               name_to_update=name_to_update,
                               id=id)

    @app.route('/delete/<int:id>')
    @login_required
    def delete(id):
        username = None
        form = Sign_up()
        user_to_delete = User.query.get_or_404(id)

        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash('user deleted successfully!')

            our_users = User.query.order_by(User.date_add)
            return render_template("signup.html",
                                   form=form,
                                   username=username,
                                   our_users=our_users)
        except:

            flash('user not found! try again')
            return render_template("signup.html",
                                   form=form,
                                   username=username,
                                   our_users=our_users)

    @app.route('/logout', methods=['GET', 'POST'])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/events')
    @login_required
    def events():
        posts = Posts.query.filter_by(
            author=current_user.id).order_by(Posts.date_posted)
        return render_template("maindashboard.html", posts=posts)
    
    @app.route('/events/edit_event/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit_event(id):
        post = Posts.query.get_or_404(id)
        form = EditEventForm(obj=post)
        if form.validate_on_submit():
            post.title = form.title.data
            post.slug = form.slug.data
            post.place = form.place.data
            if form.image.data:
                file = request.files['image']
                filename = secure_filename(file.filename)
                image_name = str(uuid.uuid1()) + '_' + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name))
                post.image = image_name

            db.session.commit()
            flash('Post been updated', 'success')
            return redirect(url_for('events', id=post.id))
        return render_template('edit_event.html', form=form, post=post)

    @app.route('/creat-event', methods=['GET', 'POST'])
    @login_required
    def create_event():
        form = PostForm()
        post = None
        if form.validate_on_submit():
            post = Posts(title=form.title.data,
                         author=current_user.id, slug=form.slug.data, start=form.start.data,
                         end=form.end.data, place=form.place.data)
            if 'image' in request.files:
                file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                image_name = str(uuid.uuid1()) + '_' + filename
                file.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], image_name))
                post.image = image_name
            form.title.data = ''
            form.slug.data = ''
            form.start.data = ''
            form.end.data = ''
            form.place.data = ''
            db.session.add(post)
            db.session.commit()
            flash('Event Post was submited successfuly')
            return redirect(url_for('dashboard'))
        return render_template('create_event.html', post=post ,form=form)

    @app.route('/events/delete/<id>', methods=['GET', 'POST'])
    @login_required
    def delete_event(id):
        post = Posts.query.get_or_404(id)
        if post:
            db.session.delete(post)
            db.session.commit()
            flash('Event post was deleted')
            return redirect(url_for("events"))
        else:
            flash('whoops! there was a problem deleting post, try again...')
        return render_template("maindashboard.html", posts=post)

    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    @app.route('/invite')
    @login_required
    def invite():
        invite_url = url_for('invite', _external=True)
        return render_template("invite.html")


    @app.route('/tirms')
    def tirms():
        return render_template('tirms.html')
    
    @app.route('/aboutus')
    def about():
        return render_template('aboutus.html')
    
    @app.route('/dashboard', methods=['GET', 'POST'])
    @login_required
    def dashboard():
        post = Posts.query.all()
        id = current_user.id
        return render_template('dashboard.html', id=id, post=post)

    @app.route('/calander')
    @login_required
    def calander():
        posts = Posts.query.all()
        return render_template('calander.html', posts=posts)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404
    # internal server error

    @app.errorhandler(500)
    def page_not_found(e):
        return render_template("500.html"), 500

    with app.app_context():
        db.create_all()

    return app
