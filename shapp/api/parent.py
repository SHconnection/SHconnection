from flask import jsonify, request, g
from . import api
from ..models import Parent, Child, Theclass
from .. import db
from .decorators import parent_login_required, login_required


@api.route('/parent/addclass/<int:classid>/', methods=['POST'])
def parentinit(classid):
    cls = Theclass.query.filter_by(id=classid).first() or None
    if not cls:
        return jsonify({"msg": "class not fonund"}), 404

    sid = request.get_json().get("sid")
    password = request.get_json().get("password")
    if sid is None or password is None:
        return jsonify({"msg": "need sid, password"}), 400

    p = Parent.query.filter_by(sid=sid).first() or None
    if p:
       return jsonify({"msg": "parent already signed up"}), 400

    # 查找孩子是否存在
    child = Child.query.filter_by(sid=sid).first() or None
    if not child:
        return jsonify({"msg": "child not found"}), 404


    p = Parent(
        sid = sid,
        name = child.name + "'s parent",
        password=password,
        child_id=child.id,
        class_id=cls.id
    )
    db.session.add(p)
    db.session.commit()

    return jsonify({'pid': p.id}), 200


@api.route("/parent/signin/", methods=["POST"])
def parent_signin():
    sid = request.get_json().get("sid")
    password = request.get_json().get("password")
    p = Parent.query.filter_by(sid=sid).first() or None
    if not p:
        return jsonify({"msg": "not found"}), 404

    if not p.verify_password(password):
        return jsonify({'msg': 'password wrong'}), 400
    token = p.generate_confirmation_token()
    return jsonify({ 
        'token' : token,
        'class_id': p.class_id,
        }), 200

@api.route('/parent/profile/',methods=['POST'])
@parent_login_required
def edit_parent_profile():
    """
    家长修改通讯录资料
    :return:
    """
    p = g.current_user
    tel = request.get_json().get('tel')
    name = request.get_json().get('name')
    wechat = request.get_json().get('wechat')
    intro = request.get_json().get('intro')
    avatar = request.get_json().get('avatar')
    relation = request.get_json().get('relation')

    tmp = Parent.query.filter_by(tel=tel).first()
    if tmp is not None and tmp is not p:
        return jsonify({'msg': '电话已注册，不能使用次电话!'}), 403

    p.tel = tel
    p.name = name
    p.wechat = wechat
    p.intro = intro
    p.avatar = avatar
    p.ralation = relation

    db.session.add(p)
    db.session.commit()

    return jsonify({ 'msg' : 'edited!'}), 200



@api.route('/parent/info/',methods=['GET'])
@login_required
def get_parent_profile():
    """
    获得家长通讯录资料
    :return:
    """
    pid = request.args.get("pid",type=int)
    p = Parent.query.filter_by(id=pid).first()
    if p is None:
        return jsonify({ 'msg' : 'no such parent'}), 404

    return jsonify(p.json_info()), 200

# 废弃
@api.route('/parent/signup/',methods=['POST'])
def parent_signup():
    """
    家长注册
    :return:
    """
    tel = request.get_json().get('tel')
    password = request.get_json().get('password')
    name = request.get_json().get('name')
    childid = request.get_json().get('childid')
    
    if tel is None or password is None or name is None or childid is None:
        return jsonify({ 'msg' : '注册信息不全'}), 403

    p = Parent.query.filter_by(tel=tel).first()
    if p is not None:
        return jsonify({ 'msg' : '电话已注册!'}), 401

    c = Child.query.filter_by(id=childid).first()
    if c is None:
        return jsonify({ 'msg' : '孩子不存在！'}), 403
    else:
        class_id = c.class_id

    p = Parent(
        name=name,
        password=password,
        child_id=childid,
        tel=tel,
        class_id = class_id,
    )

    db.session.add(p)
    db.session.commit()

    return jsonify({ 'pid' : p.id }), 200

# 废弃
@api.route('/parent/login/',methods=['POST'])
def parent_login():
    """
    家长登录
    :return:
    """
    tel = request.get_json().get('tel')
    password = request.get_json().get('password')

    if tel is None or password is None:
        return jsonify({ 'msg' : '登录信息不全! '}) , 401

    p = Parent.query.filter_by(tel=tel).first()
    if p is None:
        return jsonify({ 'msg' : '电话未注册!' }), 401

    if not p.verify_password(password):
        return jsonify({ 'msg' : '密码错误!'}), 401

    token = p.generate_confirmation_token()
    return jsonify({ 'token' : token }), 200



