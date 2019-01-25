from flask import jsonify, request, g
from . import api
from ..models import Teacher, Parent, TEvaluation, PEvaluation, TScore, PScore, Child, Theclass
from .. import db
from .decorators import parent_login_required, login_required, teacher_login_required


@api.route("/chart/", methods = ["GET"])
@parent_login_required
def getchart():
    pass


@api.route("/chart/test/", methods = ["GET"])
def chart_test():
    chartData = {
            "chartData":
                {
                    "columns": ["日期","活动水平", "作息规律", "情绪状况", "专注力", "礼貌素质"],
                    "rows": [
                        {
                            "日期": "1/1",
                            "活动水平": "20",
                            "作息规律": "20",
                            "情绪状况": "20",
                            "专注力": "20",
                            "礼貌素质": "20"
                        },
                        {
                            "日期": "1/2",
                            "活动水平": "13",
                            "作息规律": "15",
                            "情绪状况": "16",
                            "专注力": "17",
                            "礼貌素质": "18"
                        },
                        {
                            "日期": "1/3",
                            "活动水平": "19",
                            "作息规律": "18",
                            "情绪状况": "17",
                            "专注力": "17",
                            "礼貌素质": "16"
                        },
                        {
                            "日期": "1/4",
                            "活动水平": "12",
                            "作息规律": "10",
                            "情绪状况": "8",
                            "专注力": "6",
                            "礼貌素质": "5"
                        },
                        {
                            "日期": "1/5",
                            "活动水平": "14",
                            "作息规律": "15",
                            "情绪状况": "16",
                            "专注力": "13",
                            "礼貌素质": "12"
                        },
                        {
                            "日期": "1/6",
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