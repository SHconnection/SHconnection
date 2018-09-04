import time
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime
import base64

# 多对多
Teacher2Class = db.table(
    'class_teacher_maps',
    db.Column('class_id',db.Integer,db.ForeignKey('classes.id')),
    db.Column('teacher_id',db.Integer,db.ForeignKey('teachers.id'))
)

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    # 是否为班主任
    ismain = db.Column(db.Boolean, default = False)
    # 任课类型
    kind = db.Column(db.String(10))
    avatar = db.Column(db.String(100))
    tel = db.Column(db.String(20))
    wechat = db.Column(db.String(20))
    intro = db.Coulumn(db.Text)
    password_hash = db.Column(db.String(164)
    feeds = db.relationship('Feed',backref='teacher',lazy='dynamic')
    comments = db.relationship('TComment',backref='teacher',lazy='dynamic')
    evaluations = db.relationship('TEvaluation',backref='teacher',lazy='dynamic')


    @property
    def password(self):
        raise AttributeError("不能读取密码!")

    @password.setter
    def password(self,password):
        password = base64.b64decode(password)
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

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
    childs = db.relationship('Child',backref='theclass',lazy='dynamic')
    feeds = db.relationship('Feed',backref='theclass',lazy='dynamic')

    teachers = db.relationship(
        'Teacher',
        seconddary = Teacher2Class,
        backref = db.backref('classes',lazy='dynamic'),
        lazy = 'dynamic',
    )


class Child(db.Model):
    __tablename__ = 'childs'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    sid = db.Column(db.String(30))
    class_id = db.Column(db.Integer,db.ForeignKey('classes.id'))
    parents = db.relationship('Parent',backref='childs',lazy='dynamic')
    pevaluations = db.relationship('PEvaluation',backref='child',lazy='dynamic')
    tevaluations = db.relationship('TEvaluation',backref='child',lazy='dynamic')



class Parent(db.Model):
    __tablename__ = 'parents'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    avatar = db.Column(db.String(100))
    tel = db.Column(db.String(20))
    wechat = db.Column(db.String(20))
    intro = db.Coulumn(db.Text)
    replation = db.Column(db.String(20))
    password_hash = db.Column(db.String(164))
    child_id = db.Column(db.Integer,db.ForeignKey('childs.id'))
    comments = db.relationship('PComment',backref='parent',lazy='dynamic')
    evaluations = db.relationship('PEvaluation',backref='parent',lazy='dynamic')

    @property
    def password(self):
        raise AttributeError("不能读取密码!")

    @password.setter
    def password(self,password):
        password = base64.b64decode(password)
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

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


class Feed(db.Model):
    __tablename__ = 'feeds'
    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.DateTime,default=datetime.now)
    class_id = db.Column(db.Integer,db.ForeignKey('classes.id'))
    teacher_id = db.Column(db.Integer,db.ForeignKey('teachers.id'))
    thetype = db.Column(db.String(20))
    content = db.Column(db.Text)
    likes = db.Column(db.Integer)
    pcomments = db.relationship('Pcomment',backref='feeds',lazy='dynamic')
    tcomments = db.relationship('Tcomment',backref='feeds',lazy='dynamic')


# 家长评论
class PComment(db.Model):
    __tablename__ = 'pcomments'
    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.DateTime,default=datetime.now)
    content = db.Column(db.Text)
    likes = db.Column(db.Integer,default=0)
    feed_id = db.Column(db.Integer,db.ForeignKey("feeds.id"))
    parent_id = db.Column(db.Integerm,db.ForeignKey('parents.id'))


# 老师评论
class TComment(db.Model):
    __tablename__ = 'tcomments'
    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.DateTime,default=datetime.now)
    content = db.Column(db.Text)
    likes = db.Column(db.Integer,default=0)
    feed_id = db.Column(db.Integer,db.ForeignKey("feeds.id"))
    teacher_id = db.Column(db.Integerm,db.ForeignKey('teachers.id'))


# 家长评价
class PEvaluation(db.Model):
    __tablename__ = 'pevaluations'
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text)
    # datetime.datetime.now()
    time = db.Column(db.DateTime,default=datetime.now)
    parent_id = db.Column(db.Integer,db.ForeignKey('parents.id'))
    child_id = db.Column(db.Integer,db.ForeignKey('childs.id'))
    scores = db.relationship('PScore',backref='pevaluation',lazy='dynamic')

#老师评价
 class TEvaluation(db.Model):
    __tablename__ = 'tevaluations'
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text)
    # datetime.datetime.now()
    time = db.Column(db.DateTime,default=datetime.now)
    teacher_id = db.Column(db.Integer,db.ForeignKey('teachers.id'))
    child_id = db.Column(db.Integer,db.ForeignKey('childs.id'))
    scores = db.relationship('TScore',backref='tevaluation',lazy='dynamic')

#家长评分
class PScore(db.Model):
    __tablename__ = 'pscores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    score = db.Column(db.Float)
    evaluation_id = db.Column(db.Integer,db.ForeignKey('pevaluations.id'))

#老师评分
class TScore(db.Model):
    __tablename__ = 'tscores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    score = db.Column(db.Float)
    evaluation_id = db.Column(db.Integer,db.ForeignKey('tevaluations.id'))

