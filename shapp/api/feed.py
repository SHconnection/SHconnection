from flask import jsonify, request, g
from . import api
from ..models import Teacher, Parent, Feed, PComment, TComment
from .. import db
from .decorators import parent_login_required, login_required, teacher_login_required


@api.route('/feed/',methods=['POST'])
@teacher_login_required
def teacher_send_feed():
    """
    老师发送feed流 　
    :return:
    """
    t = g.current_user
    classid = request.get_json().get("classId")
    tid = request.get_json().get("teacherId")
    thetype = request.get_json().get("type")
    content = request.get_json().get("content")

    feed = Feed
    feed.class_id = classid
    feed.teacher_id = tid
    feed.thetype = thetype
    feed.content = content

    db.session.add(feed)
    db.session.commit()

    return jsonify({ 'created' : feed.id }), 201



