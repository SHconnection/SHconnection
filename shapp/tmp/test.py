from kmeans import Kmeans
import pprint

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

def kkmeans():
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

    """
    data_all = {
        "data": {
            "columns":['日期', '孩子1','孩子2','孩子3','孩子4','孩子5','孩子6','孩子7','孩子8','孩子9','孩子10','孩子11','孩子12','孩子13','孩子14','孩子15','孩子16','孩子17','孩子18','孩子19','孩子20'],
            "rows": [data1.get("data").get("rows") + data2.get("data").get("rows") + data3.get("data").get("rows")]
        }
    }
    """
    pprint.pprint(data1)
    pprint.pprint(data2)
    pprint.pprint(data3)
    pprint.pprint(data_all)


if __name__ == '__main__':
    kkmeans()
