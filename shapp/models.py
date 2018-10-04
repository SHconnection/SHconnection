import time
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime
import base64

# 多对多
Teacher2Class = db.Table(
    'class_teacher_maps',
    db.Column('class_id',db.Integer,db.ForeignKey('theclasses.id')),
    db.Column('teacher_id',db.Integer,db.ForeignKey('teachers.id'))
)

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    # 是否为班主任
    ismain = db.Column(db.Boolean, default = False)
    # 任课类型，它是任课类型
    kind = db.Column(db.String(10))
    # 工号
    wid = db.Column(db.String(20))
    avatar = db.Column(db.String(100))
    tel = db.Column(db.String(20))
    wechat = db.Column(db.String(20))
    intro = db.Column(db.Text)
    password_hash = db.Column(db.String(164))
    feeds = db.relationship('Feed',backref='teacher',lazy='dynamic')
    #comments = db.relationship('Comment',backref='teacher',lazy='dynamic')
    evaluations = db.relationship('TEvaluation',backref='teacher',lazy='dynamic')


    @property
    def password(self):
        raise AttributeError("不能读取密码!")

    @password.setter
    def password(self,password):
        password = password
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 8 months
    def generate_confirmation_token(self, expiration=20736000):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'usertype':'teacher', 'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_confirmation_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return None
        return Teacher.query.get(data['id'])

    def json_info(self):
        info = {
            'tel' : self.tel,
            'name' : self.name,
            'wechat' : self.wechat,
            'intro' : self.intro,
            'avatar' : self.avatar,
        }
        return info

    def brief_info(self):
        info = {
            'id': self.id,
            'name' : self.name,
            'avatar' : self.avatar,
        }
        return info



class Theclass(db.Model):
    __tablename__ = 'theclasses'
    id = db.Column(db.Integer, primary_key = True)
    classname = db.Column(db.String(30))
    # 班主任工号
    mainteacher_id = db.Column(db.String(20))
    childs = db.relationship('Child',backref='theclass',lazy='dynamic')
    feeds = db.relationship('Feed',backref='theclass',lazy='dynamic')

    teachers = db.relationship(
        'Teacher',
        secondary = Teacher2Class,
        backref = db.backref('theclasses',lazy='dynamic'),
        lazy = 'dynamic',
    )


class Child(db.Model):
    __tablename__ = 'childs'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    sid = db.Column(db.String(30))
    class_id = db.Column(db.Integer,db.ForeignKey('theclasses.id'))
    parents = db.relationship('Parent',backref='child',lazy='dynamic')
    pevaluations = db.relationship('PEvaluation',backref='child',lazy='dynamic')
    tevaluations = db.relationship('TEvaluation',backref='child',lazy='dynamic')



class Parent(db.Model):
    __tablename__ = 'parents'
    id = db.Column(db.Integer, primary_key = True)
    # 孩子的学号
    sid = db.Column(db.String(20))
    name = db.Column(db.String(30))
    avatar = db.Column(db.String(100))
    tel = db.Column(db.String(20))
    wechat = db.Column(db.String(20))
    intro = db.Column(db.Text)
    relation = db.Column(db.String(20))
    password_hash = db.Column(db.String(164))
    child_id = db.Column(db.Integer,db.ForeignKey('childs.id'))
    # comments = db.relationship('Comment',backref='parent',lazy='dynamic')
    evaluations = db.relationship('PEvaluation',backref='parent',lazy='dynamic')
    class_id = db.Column(db.Integer)

    @property
    def password(self):
        raise AttributeError("不能读取密码!")

    @password.setter
    def password(self,password):
        password = password
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=20736000):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'usertype':'parent', 'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_confirmation_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return None
        return Parent.query.get(data['id'])

    def json_info(self):
        info = {
            'tel' : self.tel,
            'name' : self.name,
            'wechat' : self.wechat,
            'intro' : self.intro,
            'avatar' : self.avatar,
            'relation' : self.relation,
        }
        return info

    def brief_info(self):
        info = {
            'tel': self.tel,
            'name' : self.name,
            'avatar' : self.avatar,
        }
        return info


class Feed(db.Model):
    __tablename__ = 'feeds'
    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.DateTime,default=datetime.now)
    class_id = db.Column(db.Integer,db.ForeignKey('theclasses.id'))
    teacher_id = db.Column(db.Integer,db.ForeignKey('teachers.id'))
    thetype = db.Column(db.String(20))
    content = db.Column(db.Text)
    likes = db.Column(db.Integer, default=0)
    # pcomments = db.relationship('PComment',backref='feeds',lazy='dynamic')
    # tcomments = db.relationship('TComment',backref='feeds',lazy='dynamic')
    comments = db.relationship('Comment',backref='feeds',lazy='dynamic')

    # 以下使用str() 与 eval(), 不使用redis 
    pictures = db.Column(db.Text, default="[]")
    readed = db.Column(db.Text, default="[]")
    readnum = db.Column(db.Integer, default=0)
    unreaded = db.Column(db.Text, default="[]")
    liked = db.Column(db.Text, default="[]")
    
    def picskey(self):
        return "feed" + str(self.id)

    def feedret(self):
        teacher = Teacher.query.filter_by(id=self.teacher_id).first()
        return {
            "id": self.id,
            "class_id": self.class_id,
            "type": self.thetype,
            "content": self.content,
            "likes": self.likes,
            "liked": False,
            "picture_urls": eval(self.pictures),
            "teacherSimpleInfo": teacher.brief_info()
        }


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key = True)
    ctype = db.Column(db.String(10))
    time = db.Column(db.DateTime,default=datetime.now)
    content = db.Column(db.Text)
    likes = db.Column(db.Integer, default=0)
    feed_id = db.Column(db.Integer, db.ForeignKey("feeds.id"))
    uid = db.Column(db.Integer)

    @staticmethod
    def makecomment(utype, uid, feed_id, content):
        if utype == "teacher":
            user = Teacher.query.filter_by(id=uid).first() or None
        elif utype == "parent":
            user = Parent.query.filter_by(id=uid).first() or None
        else:
            user = None

        if user is None:
            raise Exception
        else:
            c = Comment()
            c.ctype = utype
            c.content = content
            c.feed_id = feed_id
            c.uid = uid

            return c


    def add_user_info(self):
        if self.ctype == "teacher":
            user = Teacher.query.filter_by(id=self.uid).first() or None
        elif self.ctype == "parent":
            user = Parent.query.filter_by(id=self.uid).first() or None
        else:
            user = None

        if not user:
            user = {
                "utype": self.ctype,
                "uid": 0,
                "uname": "没找到此用户",
                "avater": "placeholder"
            }
        else:
           user = {
                "utype": self.ctype,
                "uid": self.uid,
                "uname": user.name,
                "avatar": user.avatar
            }

        return {
                    "id": self.id,
                    "feedId": self.feed_id,
                    "content": self.content,
                    "like": self.likes,
                    "user_simple_info": user
                }

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

    def to_json(self):
        data = {}
        data['content'] = self.content
        data['time'] = self.time
        data['scores'] = [ s.to_json() for s in self.scores ]
        return data

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

    def to_json(self):
        data = {}
        data['content'] = self.content
        data['time'] = self.time
        data['scores'] = [ s.to_json() for s in self.scores ]
        return data

#家长评分
class PScore(db.Model):
    __tablename__ = 'pscores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    score = db.Column(db.Float)
    evaluation_id = db.Column(db.Integer,db.ForeignKey('pevaluations.id'))

    def to_json(self):
        data = {}
        data['name'] = self.name
        data['score'] = self.score
        return data

#老师评分
class TScore(db.Model):
    __tablename__ = 'tscores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    score = db.Column(db.Float)
    evaluation_id = db.Column(db.Integer,db.ForeignKey('tevaluations.id'))

    def to_json(self):
        data = {}
        data['name'] = self.name
        data['score'] = self.score
        return data

