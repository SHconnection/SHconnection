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

    teachers = [ t.teacher_format_info() for t in c.teachers ]
    parents = []
    for child in c.childs:
        parents += [ p.parent_format_info() for p in child.parents ]

    return jsonify({
        'teacher': teachers,
        'parent': parents
    }), 200


@api.route('/init/class/',methods=['POST'])
def init_class():
    """
    创建班级
    """
    class_name = request.get_json().get('class_name')
    main_teacher_wid = request.get_json().get('main_teacher_wid')
    children = request.get_json().get('children_list')
    teachers = request.get_json().get('teachers_list')

    mainteacher = Teacher.query.filter_by(wid=main_teacher_wid).first()
    theclass = Theclass.query.filter_by(mainteacher_id=main_teacher_wid).first()

    if mainteacher is None:
        return jsonify({ 'msg' : '班主任不存在!'}), 403

    if theclass is not None:
        return jsonify({ 'msg' : '已经创建班级，不能再创建!'}), 403

    theclass = Theclass(
        classname=class_name,
        mainteacher_id=main_teacher_wid,
    )

    theclass.teachers.append(mainteacher)
    db.session.add(theclass)
    db.session.commit()

    # 班级id
    cid = theclass.id

    for each in children:
        child = Child(
            sid=each['sid'],
            name=each['name'],
            class_id=cid
        )
        db.session.add(child)
    db.session.commit()

    for each in teachers:
        teacher = Teacher(
            wid=each['wid'],
            name=each['name'],
        )
        db.session.add(teacher)
        db.session.commit()
        theclass.teachers.append(teacher)

    db.session.add(theclass)
    db.session.commit()

    return jsonify({ 'class_id' : theclass.id}), 201
