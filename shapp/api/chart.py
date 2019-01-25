from flask import jsonify, request, g
from . import api
from ..models import Teacher, Parent, TEvaluation, PEvaluation, TScore, PScore, Child, Theclass
from .. import db
from .decorators import parent_login_required, login_required, teacher_login_required

from operator import itemgetter

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