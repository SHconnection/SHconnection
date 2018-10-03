from flask import jsonify, request, g
from . import api
from ..models import Teacher, Parent, Feed, Comment
from .. import db
from .decorators import parent_login_required, login_required, teacher_login_required
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


@api.route('/feed/',methods=['POST'])
#@teacher_login_required
def teacher_send_feed():
    """
    老师发送feed流 　
    :return:
    """

    token = request.headers['Token'].encode('utf-8')
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
        teacherid = data['id']
    except:
        return jsonify({"msg": "auth error"}), 401

    feed = Feed()
    feed.class_id = request.get_json().get("classId")
    feed.teacher_id = request.get_json().get("teacherId")
    feed.thetype = request.get_json().get("type")
    feed.content = request.get_json().get("content")
    feed.picture_urls = str(request.get_json().get("picture_urls"))
    
    # init unread people 
    unreaded = []
    parents = Parent.query.filter_by(class_id = feed.class_id).all()
    for p in parents:
        unreaded.append(p.id)
    feed.unreaded = str(unreaded)
    feed.readed = str([])
    feed.liked = str([])

    db.session.add(feed)
    db.session.commit()

    return jsonify({'created':feed.id}), 201

@api.route('/feeds/<int:pagenum>/')
#@login_required
def getfeeds(pagenum):
    pageSize = 10
    rows = db.session.query(Feed).filter(Record == Value).count()
    pageMax = rows / pageSize
    if rows % pageSize:
        pageMax += 1
    hasnext = True
    if pagenum > pageMax:
        hasnext = False
    feeds = db.session.query(Feed).limit(pageSize).offset((pagenum-1)*pageSize)
    feedsret = [feed.feedret() for feed in feeds]
    return jsonify({
        "pagenum": pagenum,
        "nums": len(feeds),
        "hasnext": hasnext,
        "feeds": feedsret
    })


@api.route('/feed/<int:feedid>/')
#@login_required
def get_a_feed(feedid):
    feed = Feed.query.filter_by(id=feedid).first() or None
    if feed:
        teacher = Teacher.query.filter_by(id = feed.teacher_id).first() or None
        if not teacher:
            return jsonify({"msg": "teacher not found"}), 404
        
        try:
            teacher_simple_info = teacher.brief_info        
            readed = eval(feed.readed)
            unreaded = eval(feed.unreaded)
            
            likes_person = eval(feed.liked)

            token = request.headers['Token'].encode('utf-8')
            s = Serializer(current_app.config['SECRET_KEY'])
            try:
                data = s.loads(token)
                uid = data['id']
            except:
                return jsonify({"msg": "auth error"}), 401
            if uid in likes_person:
                liked = True
            else:
                liked = False

            likenum = len(liked)
            pictures = eval(feed.pictures)
        except:
            return jsonify({"msg": "server error"}), 500

        return jsonify({
                "feedinfo": {
                        "id": feed.id,
                        "classId": feed.class_id,
                        "type": feed.thetype,
                        "content": feed.content,
                        "likes": likenum,
                        "liked": liked,
                        "picture_urls": pictures,
                        "teacherSimpleInfo": teacher_simple_info
                    },
                "readed": readed,
                "unreaded": unreaded
            })
    else:
        return jsonify({
                "msg": "feed not found"
            }), 404


@api.route('/feed/<int:feedid>/read/')
#@parent_login_required
def readfeed(feedid):
    pid = request.get_json().get("pid")
    thefeed = Feed.query.filter_by(id=feedid).first()
    if thefeed is None:
        return jsonify({"msg": "notfound"}), 404
    else:
        readedlist = eval(thefeed.readed)
        unreadedlist = eval(thefeed.unreaded)
        readedlist.append(int(pid))
        unreadedlist.remove(int(pid))
        
        thefeed.readed = str(readedlist)
        thefeed.unreaded = str(unreadedlist) 
        thefeed.readnum = thefeed.readnum + 1

        db.session.commit()

        return jsonify({"msg": "ok"}), 200

@api.route('/feed/<int:feedid>/like/')
#@login_required
def likefeed(feedid):

    token = request.headers['Token'].encode('utf-8')
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
        uid = data['id']
        utype = data['usertype']
        utypeid = utype + str(uid)
    except:
        return jsonify({"msg": "auth error"}), 401

    thefeed = Feed.query.filter_by(id=feedid).first()
    if thefeed is None:
        return jsonify({"msg": "notfound"}), 404
    else:
        likelist = eval(thefeed.liked)
        if utypeid in likelist:
            return jsonify({"msg": "forbidden"}), 403
        else:
            likelist.append(utypeid)
            thefeed.liked = str(likelist)
            thefeed.likes += 1
            db.session.commit()

@api.route('/feed/<int:feedid>/comment/')
def makecomment(feedid):

    token = request.headers['Token'].encode('utf-8')
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
        uid = data['id']
        utype = data['usertype']
    except:
        return jsonify({"msg": "auth error"}), 401

    feedid = request.get_json().get("feedId")
    content = request.get_json().get("content")

    try:
        c = Comment.makecomment(utype, uid, feedid, content)
    except:
        return jsonify({"msg": "info error"}), 400
    db.session.add(c)
    db.session.commit(c)
    return jsonify({"msg": utype + " comment for feed " + str(feedid) + "posted."}), 201

@api.route('/feed/{int:feedid}/comments/')
def getcomments(feedid):
    feed = Feed.query.filter_by(id=feedid).first() or None
    if feed:
        comments = Comment.query.filter_by(feed_id=feedid).all()
        for c in comments:
            c = c.add_user_info()
        return jsonify({
                "comments": comments
            })
    else:
        return jsonify({"msg": "feed not found"}), 404


