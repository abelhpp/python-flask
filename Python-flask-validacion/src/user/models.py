import ast, os
from src.extinsions import db
from sqlalchemy.event import listens_for

basedir = os.path.abspath(os.path.dirname(__file__))

likes = db.Table('likes',
                 db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                 db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
                 )

class Comment(db.Model):
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
    body = db.Column(db.String(50))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    caption = db.Column(db.String(50))
    images = db.Column(db.String(100), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    get_images = lambda self : ast.literal_eval(self.images)


@listens_for(Post, "after_delete")
def delete_images(mapper, connection, target):
    for image in target.get_images():
        try :
            os.remove(os.path.join(basedir, 'static/images/', image))
        except OSError:
            pass



from src.extinsions import s, db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
#from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))

class Follow(db.Model):
    followed_id = db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
    follower_id = db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)

class User(db.Model, UserMixin):
        __searchable__ = ['username', 'name']

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), nullable=False)
        username = db.Column(db.String(80), unique=True, nullable=False)
        avatar = db.Column(db.String(120), nullable = False, default = 'default.svg')
        email = db.Column(db.String(120), unique=True, nullable=False)
        password = db.Column(db.String(200), unique=True, nullable=False)
        is_confirmed = db.Column(db.Boolean, default=True)
        posts = db.relationship('Post', backref='user', lazy='dynamic')
        comments = db.relationship('Comment', backref='user', lazy='dynamic')
        posts_liked = db.relationship('Post', secondary=likes, backref='user_liked', lazy='dynamic')
        followed = db.relationship('Follow', foreign_keys=[Follow.follower_id],
                                   backref=db.backref('follower', lazy='joined'),
                                   lazy='dynamic', cascade='all, delete-orphan')
        followers = db.relationship('Follow', foreign_keys=[Follow.followed_id],
                                   backref=db.backref('followed', lazy='joined'),
                                   lazy='dynamic', cascade='all, delete-orphan')

        def set_password(self, password):
            self.password = generate_password_hash(password)

        def check_password(self, password):
            return check_password_hash(self.password, password)

        

        def get_serializer_token(self, expires_sec=600, salt='default'):
            ss = s.loads(current_app.config['SECRET_KEY'], expires_sec, salt=salt)
            return ss.dumps({'user_id': self.id}).decode('utf-8')

        @staticmethod
        def verify_serializer_token(token, salt='default'):
            s = s.loads(current_app.config['SECRET_KEY'], salt=salt)
            try:
             user_id = s.loads(token)['user_id']
            except:
             return None
            return User.query.get(user_id)

        def is_following(self, user):
            return self.followed.filter_by(followed_id=user.id).first() is not None

        def is_followed_by(self, user):
            return self.followers.filter_by(follower_id=user_id).first() is not None

        def follow(self, user):
            if not self.is_following(user):
                f = Follow(follower=self, followed=user)
                db.session.add(f)

        def unfollow(self, user):
            f = self.followed.filter_by(followed_id=user.id).first()
            if f :
                db.session.delete(f)

        @property
        def self_follow(self):
            self.follow(self)

        @property
        def followed_posts(self):
            return Post.query.join(Follow, Follow.followed_id == Post.user_id)\
                    .filter(Follow.follower_id == self.id)

        @property
        def all_followed(self):
            return [ f.followed for f in self.followed.filter(Follow.followed_id != self.id).all() ]

        @property
        def all_followers(self):
            return [ f.follower for f in self.followers.filter(Follow.follower_id != self.id).all() ]