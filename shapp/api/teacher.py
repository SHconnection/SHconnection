from flask import jsonify, request, g
from . import api
from ..models import Teacher, Theclass
from .. import db
from .decorators import teacher_login_required, login_required


@api.route('/teacher/signup/',methods=['POST'])
def teacher_signup():
    """
    老师注册
    :return:
    """
    tel = request.get_json().get('tel')
    password = request.get_json().get('password')
    name = request.get_json().get('name')
    typeid = request.get_json().get('typeid')

    if Teacher.query.filter_by(tel=tel).first() is not None:
        return jsonify({ 'msg' : '电话已注册!'}), 401
    if tel is None or password is None or name is None or typeid is None:
        return jsonify({ 'msg' : '信息不全!'}), 403

    t = Teacher(
        name = name,
        tel = tel,
        password = password,
        ismain = (typeid=="0"),
    )

    db.session.add(t)
    db.session.commit()

    return jsonify({ 'create' : t.id }), 200



@api.route('/teacher/login/',methods=['POST'])
def teacher_login():
    """
    老师登录，登录时，加入相应的登录班级，顺便将教师加入该班级
    :return:
    """
    tel = request.get_json().get('tel')
    password = request.get_json().get('password')
    cid = request.get_json().get('cid')

    if tel is None or password is None:
        return jsonify({ 'msg' : '登录信息不全! '}) , 401

    t = Teacher.query.filter_by(tel=tel).first()
    if t is None:
        return jsonify({ 'msg' : '电话未注册!' }), 401

    if not t.verify_password(password):
        return jsonify({ 'msg' : '密码错误!'}), 401

    token = t.generate_confirmation_token()

    c = Theclass.query.filter_by(id=cid).first()
    # 老师不在班级中，加入班级
    if c is not None and t not in c.teachers:
        c.teachers.append(t)
        db.session.add(c)
        db.session.commit()

    return jsonify({ 'token' : token }), 200



@api.route('/teacher/profile/',methods=['PUT'])
@teacher_login_required
def edit_teacher_profile():
    """
    老师修改通讯录资料
    :return:
    """
    t = g.current_user
    tel = request.get_json().get('tel')
    name = request.get_json().get('name')
    wechat = request.get_json().get('wechat')
    intro = request.get_json().get('intro')
    avatar = request.get_json().get('avatar')

    tmp = Teacher.query.filter_by(tel=tel).first()
    if tmp is not None and tmp is not t:
        return jsonify({'msg': '电话已注册，不能使用次电话!'}), 403

    t.tel = tel
    t.name = name
    t.wechat = wechat
    t.intro = intro
    t.avatar = avatar

    db.session.add(t)
    db.session.commit()

    return jsonify({ 'msg' : 'edited!'}), 200




@api.route('/teacher/info/',methods=['GET'])
@login_required
def get_teacher_profile():
    """
    获得老师通讯录资料
    :return:
    """
    tid = request.args.get('tid',type=int)
    t = Teacher.query.filter_by(id=tid).first()
    if t is None:
        return jsonify({ 'msg' :'no such teacher'}), 404

    return jsonify(t.json_info()), 200
