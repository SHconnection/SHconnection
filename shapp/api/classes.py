from flask import jsonify, request, g
from . import api
from ..models import Teacher, Parent, Theclass, Child
from .. import db
from .decorators import parent_login_required, login_required, mainteacher_login_required


@api.route('/class/',methods=['POST'])
@mainteacher_login_required
def main_teacher_create_class():
    """
    班主任创建班级
    :return:
    """
    classname = request.get_json().get('classname')
    t = g.current_user

    theclass = Theclass()
    theclass.classname = classname
    theclass.mainteacher_id = t.id
    theclass.teachers.append(t)

    db.session.add(theclass)
    db.session.commit()

    return jsonify({ 'cid' : theclass.id }), 200



@api.route('/class/child/',methods=['POST'])
@mainteacher_login_required
def main_teacher_load_children():
    """
    班主任导入孩子
    :return:
    """
    cid = request.args.get("cid")
    json_data = request.get_json().get("children")
    t = g.current_user

    theclass = Theclass.query.filter_by(id=cid).first()

    if theclass is None or theclass.mainteacher_id != t.id:
        return jsonify({ 'msg' : "班级不存在或班主任错误！"}), 403

    for each in json_data:
        child = Child()
        child.name = each['name']
        child.sid = each['sid']
        child.class_id = cid
        db.session.add(child)

    db.session.commit()

    return jsonify({ 'msg' : '导入成功'}), 200


@api.route('/class/info/',methods=['GET'])
@login_required
def get_class_info():
    """
    返回班级通讯录
    :return:
    """
    cid = request.args.get('cid')
    c = Theclass.query.filter_by(id=cid).first()
    if c is None:
        return jsonify({'msg' : '班级不存在'}), 404

    teachers = [ t.brief_info() for t in c.teachers ]
    parents = []
    for child in c.childs:
        parents += [ p.brief_info() for p in child.parents ]

    return  jsonify({'teacher' : teachers,
                     'parent': parents
                     }), 200
