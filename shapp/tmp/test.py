from kmeans import Kmeans
import pprint


def kmeans_fake():
    res =  [
        {
            "data": {
                "columns": [
                    "日期",
                    "赵泽林",
                    "钱阳",
                    "孙妍菲",
                    "李怡萱",
                    "周新文",
                    "吴家豪",
                    "郑雅忆",
                    "冯子恒",
                    "陈鸿宇"
                ],
                "rows": [
                    {
                        "": 1,
                        "孩子2": 18,
                        "孩子3": 7,
                        "孩子4": 20,
                        "孩子5": 18,
                        "孩子6": 15,
                        "孩子7": 1,
                        "孩子8": 0,
                        "孩子9": 17,
                        "日期": 1
                    },
                    {
                        "孩子1": 8,
                        "孩子2": 18,
                        "孩子3": 19,
                        "孩子4": 15,
                        "孩子5": 16,
                        "孩子6": 15,
                        "孩子7": 20,
                        "孩子8": 16,
                        "孩子9": 20,
                        "日期": 2
                    },
                    {
                        "孩子1": 20,
                        "孩子2": 1,
                        "孩子3": 14,
                        "孩子4": 8,
                        "孩子5": 17,
                        "孩子6": 13,
                        "孩子7": 1,
                        "孩子8": 18,
                        "孩子9": 13,
                        "日期": 3
                    },
                    {
                        "孩子1": 19,
                        "孩子2": 19,
                        "孩子3": 17,
                        "孩子4": 3,
                        "孩子5": 6,
                        "孩子6": 19,
                        "孩子7": 17,
                        "孩子8": 20,
                        "孩子9": 9,
                        "日期": 4
                    },
                    {
                        "孩子1": 4,
                        "孩子2": 4,
                        "孩子3": 11,
                        "孩子4": 12,
                        "孩子5": 0,
                        "孩子6": 11,
                        "孩子7": 4,
                        "孩子8": 16,
                        "孩子9": 11,
                        "日期": 5
                    },
                    {
                        "孩子1": 8,
                        "孩子2": 13,
                        "孩子3": 15,
                        "孩子4": 1,
                        "孩子5": 9,
                        "孩子6": 7,
                        "孩子7": 3,
                        "孩子8": 14,
                        "孩子9": 0,
                        "日期": 6
                    },
                    {
                        "孩子1": 3,
                        "孩子2": 6,
                        "孩子3": 19,
                        "孩子4": 12,
                        "孩子5": 9,
                        "孩子6": 20,
                        "孩子7": 13,
                        "孩子8": 8,
                        "孩子9": 16,
                        "日期": 7
                    },
                    {
                        "孩子1": 0,
                        "孩子2": 19,
                        "孩子3": 6,
                        "孩子4": 6,
                        "孩子5": 11,
                        "孩子6": 8,
                        "孩子7": 4,
                        "孩子8": 20,
                        "孩子9": 8,
                        "日期": 8
                    },
                    {
                        "孩子1": 0,
                        "孩子2": 4,
                        "孩子3": 8,
                        "孩子4": 0,
                        "孩子5": 2,
                        "孩子6": 14,
                        "孩子7": 2,
                        "孩子8": 5,
                        "孩子9": 16,
                        "日期": 9
                    },
                    {
                        "孩子1": 1,
                        "孩子2": 1,
                        "孩子3": 6,
                        "孩子4": 10,
                        "孩子5": 8,
                        "孩子6": 6,
                        "孩子7": 18,
                        "孩子8": 14,
                        "孩子9": 15,
                        "日期": 10
                    }
                ]
            }
        },
        {
            "data": {
                "columns": [
                    "日期",
                    "孩子1",
                    "孩子2",
                    "孩子3",
                    "孩子4"
                ],
                "rows": [
                    {
                        "孩子1": 12,
                        "孩子2": 11,
                        "孩子3": 20,
                        "孩子4": 20,
                        "日期": 1
                    },
                    {
                        "孩子1": 5,
                        "孩子2": 1,
                        "孩子3": 2,
                        "孩子4": 3,
                        "日期": 2
                    },
                    {
                        "孩子1": 4,
                        "孩子2": 7,
                        "孩子3": 2,
                        "孩子4": 12,
                        "日期": 3
                    },
                    {
                        "孩子1": 14,
                        "孩子2": 17,
                        "孩子3": 13,
                        "孩子4": 9,
                        "日期": 4
                    },
                    {
                        "孩子1": 7,
                        "孩子2": 17,
                        "孩子3": 4,
                        "孩子4": 14,
                        "日期": 5
                    },
                    {
                        "孩子1": 10,
                        "孩子2": 11,
                        "孩子3": 20,
                        "孩子4": 18,
                        "日期": 6
                    },
                    {
                        "孩子1": 16,
                        "孩子2": 10,
                        "孩子3": 0,
                        "孩子4": 17,
                        "日期": 7
                    },
                    {
                        "孩子1": 2,
                        "孩子2": 14,
                        "孩子3": 4,
                        "孩子4": 7,
                        "日期": 8
                    },
                    {
                        "孩子1": 9,
                        "孩子2": 6,
                        "孩子3": 14,
                        "孩子4": 5,
                        "日期": 9
                    },
                    {
                        "孩子1": 17,
                        "孩子2": 16,
                        "孩子3": 11,
                        "孩子4": 7,
                        "日期": 10
                    }
                ]
            }
        },
        {
            "data": {
                "columns": [
                    "日期",
                    "孩子1",
                    "孩子2",
                    "孩子3",
                    "孩子4",
                    "孩子5",
                    "孩子6",
                    "孩子7"
                ],
                "rows": [
                    {
                        "孩子1": 4,
                        "孩子2": 17,
                        "孩子3": 19,
                        "孩子4": 4,
                        "孩子5": 2,
                        "孩子6": 8,
                        "孩子7": 3,
                        "日期": 1
                    },
                    {
                        "孩子1": 7,
                        "孩子2": 7,
                        "孩子3": 11,
                        "孩子4": 14,
                        "孩子5": 2,
                        "孩子6": 12,
                        "孩子7": 2,
                        "日期": 2
                    },
                    {
                        "孩子1": 10,
                        "孩子2": 3,
                        "孩子3": 10,
                        "孩子4": 18,
                        "孩子5": 9,
                        "孩子6": 15,
                        "孩子7": 12,
                        "日期": 3
                    },
                    {
                        "孩子1": 3,
                        "孩子2": 5,
                        "孩子3": 0,
                        "孩子4": 9,
                        "孩子5": 3,
                        "孩子6": 8,
                        "孩子7": 8,
                        "日期": 4
                    },
                    {
                        "孩子1": 6,
                        "孩子2": 7,
                        "孩子3": 17,
                        "孩子4": 19,
                        "孩子5": 19,
                        "孩子6": 5,
                        "孩子7": 8,
                        "日期": 5
                    },
                    {
                        "孩子1": 4,
                        "孩子2": 20,
                        "孩子3": 2,
                        "孩子4": 19,
                        "孩子5": 18,
                        "孩子6": 18,
                        "孩子7": 5,
                        "日期": 6
                    },
                    {
                        "孩子1": 10,
                        "孩子2": 1,
                        "孩子3": 14,
                        "孩子4": 1,
                        "孩子5": 1,
                        "孩子6": 19,
                        "孩子7": 7,
                        "日期": 7
                    },
                    {
                        "孩子1": 20,
                        "孩子2": 16,
                        "孩子3": 15,
                        "孩子4": 18,
                        "孩子5": 16,
                        "孩子6": 1,
                        "孩子7": 8,
                        "日期": 8
                    },
                    {
                        "孩子1": 11,
                        "孩子2": 13,
                        "孩子3": 5,
                        "孩子4": 20,
                        "孩子5": 9,
                        "孩子6": 13,
                        "孩子7": 20,
                        "日期": 9
                    },
                    {
                        "孩子1": 10,
                        "孩子2": 3,
                        "孩子3": 6,
                        "孩子4": 7,
                        "孩子5": 20,
                        "孩子6": 4,
                        "孩子7": 3,
                        "日期": 10
                    }
                ]
            }
        }
    ]
    pprint.pprint(res)



def kmeans_helper(arr):
    names = ["赵泽林","钱阳","孙妍菲","李怡萱","周新文","吴家豪","郑雅忆","冯子恒","陈鸿宇", "韩依霖", "杨雅雯", "朱泽轩", "秦硕", "姜文浩", "孟子文", "邱思雨", "马浩杰", "余淑静", "张圣泽", "许亨哈"]
    
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
            key = names[random.randint(0, len(names)-1)]
            value = arr[ci][di]
            d.update({
                key : value
            })

        data["data"]["rows"].append(d)
    return data

def kkmeans():
    # 20孩子，每个孩子10天数据
    raw_data = '[[1, 8, 20, 19, 4, 8, 3, 0, 0, 1], [18, 18, 1, 19, 4, 13, 6, 19, 4, 1], [4, 7, 10, 3, 6, 4, 10, 20, 11, 10], [12, 5, 4, 14, 7, 10, 16, 2, 9, 17], [7, 19, 14, 17, 11, 15, 19, 6, 8, 6], [17, 7, 3, 5, 7, 20, 1, 16, 13, 3], [19, 11, 10, 0, 17, 2, 14, 15, 5, 6], [4, 14, 18, 9, 19, 19, 1, 18, 20, 7], [20, 15, 8, 3, 12, 1, 12, 6, 0, 10], [18, 16, 17, 6, 0, 9, 9, 11, 2, 8], [2, 2, 9, 3, 19, 18, 1, 16, 9, 20], [15, 15, 13, 19, 11, 7, 20, 8, 14, 6], [1, 20, 1, 17, 4, 3, 13, 4, 2, 18], [0, 16, 18, 20, 16, 14, 8, 20, 5, 14], [11, 1, 7, 17, 17, 11, 10, 14, 6, 16], [8, 12, 15, 8, 5, 18, 19, 1, 13, 4], [17, 20, 13, 9, 11, 0, 16, 8, 16, 15], [3, 2, 12, 8, 8, 5, 7, 8, 20, 3], [20, 2, 2, 13, 4, 20, 0, 4, 14, 11], [20, 3, 12, 9, 14, 18, 17, 7, 5, 7]]'
    data = eval(raw_data)
    
    kmeans = Kmeans(data, 3)
    kmeans.get_k_rand()
    kmeans.compare_to_k()
    kmeans.get_k_avarage()
    cl = kmeans.compare_to_k2()
    
    while True:
        if len(cl[0]["data"]["rows"]) < 4 or len(cl[1]["data"]["rows"]) < 4 or len(cl[2]["data"]["rows"]) < 4:
            kmeans = Kmeans(data, 3)
            kmeans.get_k_rand()
            kmeans.compare_to_k()
            kmeans.get_k_avarage()
            cl = kmeans.compare_to_k2()

    data1 = kmeans_helper(cl[0])
    data2 = kmeans_helper(cl[1])
    data3 = kmeans_helper(cl[2])
    
    data_all = kmeans_helper(cl[0] + cl[1] + cl[2])

    pprint.pprint(data1)
    pprint.pprint(data2)
    pprint.pprint(data3)
    pprint.pprint(data_all)


if __name__ == '__main__':
    kmeans()
