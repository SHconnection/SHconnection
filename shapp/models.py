import time
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(30))
    # 是否为班主任
    ismain = db.Column(db.Boolean, default = False)
    avatar = db.Column(db.String(100))
    tel = db.Column(db.String(20))
    wechat = db.Column(db.String(20))
    intro = db.Coulumn(db.String(1000))

    @staticmethod
    def generate_confirmation_token(self, expiration=604800):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False

        if data.get('confirm') != self.id:
            return False
        self.confirm = True
        db.session.add(self)
        return True

class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key = True)
    classname = db.Column(db.String(30))
    mainteacher = db.relationship('Teacher', lazy='dynamic')
    # relationship
    # class.children

class Teacher2Class(db.Model):
    __tablename__ = 'teacher2classes'
    id = db.Column(db.Integer, primary_key = True)
    theteacher = db.relationship('Teacher', lazy='dynamic')
    theclass = db.relationship('Class', lazy='dynamic')

class Child(db.Model):
    __tablename__ = 'children'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    avatar = db.Column(db.String(100))
    sid = db.Column(db.String(30))
    theclass = db.relationship('Class', backref='children', lazy='dynamic')
    # relationship
    # child.parents

class Parent(db.Model):
    __tablename__ = 'parents'
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(30))
    avatar = db.Column(db.String(100))
    tel = db.Column(db.String(20))
    wechat = db.Column(db.String(20))
    intro = db.Coulumn(db.String(1000))
    child = db.relationship('Child', backref='parents', lazy='dynamic')

    @staticmethod
    def generate_confirmation_token(self, expiration=604800):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False

        if data.get('confirm') != self.id:
            return False
        self.confirm = True
        db.session.add(self)
        return True

# read or not store in redis
class Feed(db.Model):
    __tablename__ = 'feeds'
    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.DateTime)
    theclass = db.relationship('Class', lazy='dynamic')
    teacher = db.relationship('Teacher', lazy='dynamic')
    thetype = db.Column(db.String(20))
    content = db.Column(db.String(2000))
    likes = db.Column(db.Integer)

class Comment(db.Model):
    __tablename__ = 'Comments'
    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.DateTime)
    feed = db.relationship('Feed', backref='comments', lazy='dynamic')
    content = db.Column(db.String(1000))
    likes = db.Column(db.Integer)

class Evaluation(db.Model):
    __tablename__ = 'evaluations'
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(2000))
    # datetime.datetime.now()
    time = db.Column(db.DateTime)
    # teacher or parent
    fromtype = db.Column(db.String(20))
    fromid = db.Column(db.Integer)
    score1 = db.Column(db.Float)
    score2 = db.Column(db.Float)
    score3 = db.Column(db.Float)
    score4 = db.Column(db.Float)
    score5 = db.Column(db.Float)
    score6 = db.Column(db.Float)
    score7 = db.Column(db.Float)
    score8 = db.Column(db.Float)
    score9 = db.Column(db.Float)
    score10 = db.Column(db.Float)
    score11 = db.Column(db.Float)
    score12 = db.Column(db.Float)
    score13 = db.Column(db.Float)
    score14 = db.Column(db.Float)
    score15 = db.Column(db.Float)
    score16 = db.Column(db.Float)
    score17 = db.Column(db.Float)
    score18 = db.Column(db.Float)
