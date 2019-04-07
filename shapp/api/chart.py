from flask import jsonify, request, g
from . import api
from ..models import Teacher, Parent, TEvaluation, PEvaluation, TScore, PScore, Child, Theclass
from ..kmeans import Kmeans
from .. import db
from .decorators import parent_login_required, login_required, teacher_login_required

from operator import itemgetter

import pprint

@api.route("/chart/", methods = ["GET"])
@parent_login_required
def get_chart():
    try:
        parent = g.current_user
        child = Child.query.filter_by(id=parent.child_id).first() or None
        if child is None:
            return jsonify({
                "msg": "child not found."
            })
        tes = TEvaluation.query.filter_by(child_id=child.id).all()
        pes = PEvaluation.query.filter_by(child_id=child.id).all()
        # 即便没有10个也不会报错
        tes = tes[-10:]
        pes = pes[-10:]

        tes_format_datas = [te.eval_format_data() for te in tes]
        pes_format_datas = [pe.eval_format_data() for pe in pes]
        datas = tes_format_datas + pes_format_datas
        datas = sorted(datas, key=itemgetter('time'))
        print(datas)
        rows = []
        for d in datas:
            hdsp = 0
            zxgl = 0
            qxzk = 0
            zzl = 0
            lmsz = 0
            for s in d.get("scores"):
                if s.get("key") == "活动水平":
                    hdsp = s.get("score")
                elif s.get("key") == "作息规律":
                    zxgl = s.get("score")
                elif s.get("key") == "情绪状况":
                    qxzk = s.get("score")
                elif s.get("key") == "专注力":
                    zzl = s.get("score")
                elif s.get("key") == "礼貌素质":
                    lmsz = s.get("score")
            arow = {
                "日期": d.get("time"),
                "活动水平": hdsp,
                "作息规律": zxgl,
                "情绪状况": qxzk,
                "专注力": zzl,
                "礼貌素质": lmsz
            }
            rows.append(arow)
        return jsonify(rows)
    except Exception as e:
        print(e)
        return chart_test()


@api.route("/chart/test/", methods = ["GET"])
def chart_test():
    chartData = {
            "chartData":
                {
                    "columns": ["日期","活动水平", "作息规律", "情绪状况", "专注力", "礼貌素质"],
                    "rows": [
                        {
                            "日期": "201901011001",
                            "活动水平": "20",
                            "作息规律": "20",
                            "情绪状况": "20",
                            "专注力": "20",
                            "礼貌素质": "20"
                        },
                        {
                            "日期": "201901021001",
                            "活动水平": "13",
                            "作息规律": "15",
                            "情绪状况": "16",
                            "专注力": "17",
                            "礼貌素质": "18"
                        },
                        {
                            "日期": "201901031001",
                            "活动水平": "19",
                            "作息规律": "18",
                            "情绪状况": "17",
                            "专注力": "17",
                            "礼貌素质": "16"
                        },
                        {
                            "日期": "201901041001",
                            "活动水平": "12",
                            "作息规律": "10",
                            "情绪状况": "8",
                            "专注力": "6",
                            "礼貌素质": "5"
                        },
                        {
                            "日期": "201901051001",
                            "活动水平": "14",
                            "作息规律": "15",
                            "情绪状况": "16",
                            "专注力": "13",
                            "礼貌素质": "12"
                        },
                        {
                            "日期": "201901061001",
                            "活动水平": "13",
                            "作息规律": "14",
                            "情绪状况": "18",
                            "专注力": "20",
                            "礼貌素质": "19"
                        },
                ]
            }
    }
    return jsonify(chartData)


def kmeans_helper(arr):
    cms = ['日期']
    for i in range(len(arr)):
        cms.append("孩子" + str(i+1))

    data = {
        "data": {
            "columns": cms,
            "rows": []
        }        
    }
    for di in range(len(arr[0])):
        d = {
            '日期': di+1,
        }
        for ci in range(len(arr)):
            key = '孩子' + str(ci+1)
            value = arr[ci][di]
            d.update({
                key : value
            })

        data["data"]["rows"].append(d)

    return data



@api.route("/chart/kmeans/", methods = ["GET"])
def getkmeans():
    # 20孩子，每个孩子10天数据
    raw_data = '[[1, 8, 20, 19, 4, 8, 3, 0, 0, 1], [18, 18, 1, 19, 4, 13, 6, 19, 4, 1], [4, 7, 10, 3, 6, 4, 10, 20, 11, 10], [12, 5, 4, 14, 7, 10, 16, 2, 9, 17], [7, 19, 14, 17, 11, 15, 19, 6, 8, 6], [17, 7, 3, 5, 7, 20, 1, 16, 13, 3], [19, 11, 10, 0, 17, 2, 14, 15, 5, 6], [4, 14, 18, 9, 19, 19, 1, 18, 20, 7], [20, 15, 8, 3, 12, 1, 12, 6, 0, 10], [18, 16, 17, 6, 0, 9, 9, 11, 2, 8], [2, 2, 9, 3, 19, 18, 1, 16, 9, 20], [15, 15, 13, 19, 11, 7, 20, 8, 14, 6], [1, 20, 1, 17, 4, 3, 13, 4, 2, 18], [0, 16, 18, 20, 16, 14, 8, 20, 5, 14], [11, 1, 7, 17, 17, 11, 10, 14, 6, 16], [8, 12, 15, 8, 5, 18, 19, 1, 13, 4], [17, 20, 13, 9, 11, 0, 16, 8, 16, 15], [3, 2, 12, 8, 8, 5, 7, 8, 20, 3], [20, 2, 2, 13, 4, 20, 0, 4, 14, 11], [20, 3, 12, 9, 14, 18, 17, 7, 5, 7]]'
    data = eval(raw_data)
    kmeans = Kmeans(data, 3)
    kmeans.get_k_rand()
    kmeans.compare_to_k()
    kmeans.get_k_avarage()
    cl = kmeans.compare_to_k2()
    
    data1 = kmeans_helper(cl[0])
    data2 = kmeans_helper(cl[1])
    data3 = kmeans_helper(cl[2])
    data_all = kmeans_helper(cl[0] + cl[1] + cl[2])

    return jsonify({
            "data_all": data_all,
            "k_datas": [
                data1,
                data2,
                data3,
            ]
        })
