from flask import jsonify, request, g
from . import api
from ..models import Teacher, Parent, TEvaluation, PEvaluation, TScore, PScore
from .. import db
from .decorators import parent_login_required, login_required, teacher_login_required



@api.route('/evaluation/teacher/',methods=['POST'])
@teacher_login_required
def teacher_send_evaluation():
    """
    老师发送评价
    :return:
    """
    tid = request.args.get('tid')
    cid = request.args.get('childid')

    json_data = request.get_json()
    comment = json_data['comment']
    score = json_data['score']

    te = TEvaluation()
    te.content = comment
    te.teacher_id = tid
    te.child_id = cid
    db.session.add(te)
    db.session.commit()

    for each in score:
        ts = TScore()
        ts.name = each['name']
        ts.score = each['score']
        ts.evaluation_id = te.id
        db.session.add(ts)

    db.session.commit()

    return jsonify({ 'msg' : '评价成功' }), 200

@api.route('/evaluation/teacher/all/',methods=['GET'])
@login_required
def get_teacher_evaluation():
    """
    获取老师对某一孩子的评价
    :return:
    """
    tid = request.args.get('tid')
    cid = request.args.get('childid')

    te = TEvaluation.query.filter_by(teacher_id=tid,child_id=cid).all()

    return jsonify({
        'eval' : [ t.to_json() for t in te ]
    }),200



@api.route('/evaluation/parent/',methods=['POST'])
@parent_login_required
def parent_send_evaluation():
    """
    家长发送评价
    :return:
    """
    p = g.current_user
    pid = request.args.get('pid')
    json_data = request.get_json()
    comment = json_data['comment']
    score = json_data['score']

    if p.id != int(pid):
        return jsonify({ 'msg' : '验证错误！'}), 401

    pe = PEvaluation()
    pe.content = comment
    pe.child_id = p.child_id
    pe.parent_id = p.id
    db.session.add(pe)
    db.session.commit()

    for each in score:
        ps = PScore()
        ps.name = each['name']
        ps.score = each['score']
        ps.evaluation_id = pe.id
        db.session.add(ps)

    db.session.commit()

    return jsonify({ 'msg' : '评价成功'})


@api.route('/evaluation/parent/all/',methods=['GET'])
@login_required
def get_parent_evaluation():
    """
    获取家长对某一孩子的评价
    :return:
    """
    pid = request.args.get('pid')
    cid = g.current_parent.child_id

    pe = PEvaluation.query.filter_by(parent_id=pid,child_id=cid).all()

    return jsonify({
        'eval' : [ p.to_json() for p in pe ]
    }),200
