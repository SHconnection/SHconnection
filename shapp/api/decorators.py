from functools import wraps
from flask import g , jsonify , request
from ..models import Teacher, Parent


# 老师登录
def teacher_login_required(f) :
    @wraps(f)
    def decorated(*args,**kwargs) :
        token = request.headers.get('token')
        if token is not None :
            g.current_user = Teacher.verify_confirmation_token(token)
            if g.current_user is not None :
                return f(*args,**kwargs)
            return jsonify({"msg" :"not such user!"}) , 403
        return jsonify({"msg" :"without token!"}) , 401
    return decorated


# 老师登录
def parent_login_required(f) :
    @wraps(f)
    def decorated(*args,**kwargs) :
        token = request.headers.get('token')
        if token is not None :
            g.current_user = Parent.verify_confirmation_token(token)
            if g.current_user is not None :
                return f(*args,**kwargs)
            return jsonify({"msg" :"not such user!"}) , 403
        return jsonify({"msg" :"without token!"}) , 401
    return decorated


# 老师或家长登录
def login_required(f) :
    @wraps(f)
    def decorated(*args,**kwargs) :
        token = request.headers.get('token')
        if token is not None :
            g.current_teacher = Teacher.verify_confirmation_token(token)
            g.current_parent = Parent.verify_confirmation_token(token)
            if g.current_teacher is not None or g.current_parent is not None:
                return f(*args,**kwargs)
            return jsonify({"msg" :"not such user!"}) , 403
        return jsonify({"msg" :"without token!"}) , 401
    return decorated


# 班主任登录
def mainteacher_login_required(f) :
    @wraps(f)
    def decorated(*args,**kwargs) :
        token = request.headers.get('token')
        if token is not None :
            g.current_user = Teacher.verify_confirmation_token(token)
            if g.current_user is not None and g.current_user.ismain :
                return f(*args,**kwargs)
            return jsonify({"msg" :"不是班主任!"}) , 403
        return jsonify({"msg" :"without token!"}) , 401
    return decorated