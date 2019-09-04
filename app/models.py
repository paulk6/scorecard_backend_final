from app import app, login, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import datetime
import jwt

class Club(db.Model):
    club_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400))
    address = db.Column(db.String(400))


class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('club.club_id'))
    name = db.Column(db.String(200), unique=True)
    city = db.Column(db.String(120))
    state = db.Column(db.String(75))

class Guest(db.Model):
    guest_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    phone_number = db.Column(db.String(10), unique=True)
    nickname = db.Column(db.String(120))
    handicap = db.Column(db.Integer)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'

    # create a method for generating a token and verifying that token
    def get_token(self, expires_in=86400):
        return jwt.encode(
        { 'user_id' : self.user_id, 'exp' : time() + expires_in },
        app.config['SECRET_KEY'],
        algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_token(token):
        try:
            id = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                algorithm=['HS256']
            )['user_id']
        except:
            return

        return User.query.get(id)

    def __repr__(self):
        return '<User {}>'.format(self.email)

class PlayerRound(db.Model):
    round_id = db.Column(db.Integer, primary_key=True)
    scorecard_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.guest_id'))
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'))
    hole_1_score = db.Column(db.Integer)
    hole_2_score = db.Column(db.Integer)
    hole_3_score = db.Column(db.Integer)
    hole_4_score = db.Column(db.Integer)
    hole_5_score = db.Column(db.Integer)
    hole_6_score = db.Column(db.Integer)
    hole_7_score = db.Column(db.Integer)
    hole_8_score = db.Column(db.Integer)
    hole_9_score = db.Column(db.Integer)
    hole_10_score = db.Column(db.Integer)
    hole_11_score = db.Column(db.Integer)
    hole_12_score = db.Column(db.Integer)
    hole_13_score = db.Column(db.Integer)
    hole_14_score = db.Column(db.Integer)
    hole_15_score = db.Column(db.Integer)
    hole_16_score = db.Column(db.Integer)
    hole_17_score = db.Column(db.Integer)
    hole_18_score = db.Column(db.Integer)
    total_score = db.Column(db.Integer)
