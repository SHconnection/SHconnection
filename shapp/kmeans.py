import random
import pprint
class Kmeans():

    def __init__(self, data, k):
        self.data = data 
        self.k = k 

    def get_k_rand(self):
        if len(self.data) < self.k:
            return

        size = len(self.data)
        rand_set = set()

        # 选取 k 个随机数 
        while len(rand_set) < self.k:
            rand_int = random.randint(0, size-1)
            rand_set.add(rand_int)

        rand_list = list(rand_set)
        rand_list.sort()
        self.k_list = rand_list 
        # print(self.k_list)


    def compare_to_k(self):
        self.belong = {i:[i] for i in self.k_list} 
        for i, val in enumerate(self.data):
            if i in self.k_list:
                continue
            clost = self.get_clost(self.data[i])
            self.belong[clost].append(i) 

        #print(self.belong)
    
    def get_clost(self, val):
        minn = None
        min_index = -1
        for k in self.k_list:
            now = self.calculate(self.data[k], val)
            if minn is None or minn > now:
                minn = now 
                min_index = k 
        return min_index

    
    def calculate(self, a, b):
        res = 0
        for i in range(len(a)):
            res += (a[i]-b[i])*(a[i]-b[i]) 
        return res


    def get_k_avarage(self):
        self.avar_list = list()
        for k, v in self.belong.items():
            avar = self.get_each_avarage(v)
            self.avar_list.append(avar) 
            # print(avar)    
        

    
    def get_each_avarage(self, value):
        res = list()
        data_size = len(self.data[0])
        for i in range(data_size):
            tmp = 0
            for v in value:
                tmp += self.data[v][i] 
            tmp = tmp / len(value)
            res.append(tmp)
        return res

    def compare_to_k2(self):
        self.belong2 = {i:[] for i in range(self.k) } 
        self.res_list = [[] for i in range(self.k)] 
        for i in range(len(self.data)):
            clost = self.get_clost2(self.data[i]) 
            self.belong2[clost].append(i) 
            self.res_list[clost].append(self.data[i])
        #print(self.belong2)
        #pprint.pprint(self.res_list)
        return self.res_list 
    
    def get_clost2(self, val):
        minn = None
        min_index = -1
        for i, k in enumerate(self.avar_list):
            now = self.calculate(k, val)
            if minn is None or minn > now:
                minn = now 
                min_index = i 
        return min_index
            


raw_data = '[[11, 3, 13, 13, 10, 10, 12, 2, 10, 10], [8, 13, 14, 8, 0, 4, 10, 17, 15, 7], [12, 19, 16, 12, 11, 13, 10, 2, 10, 0], [8, 3, 20, 19, 13, 9, 0, 1, 18, 16], [19, 8, 13, 4, 15, 13, 20, 17, 5, 0], [15, 4, 10, 14, 13, 3, 17, 16, 5, 4], [2, 2, 20, 0, 1, 5, 3, 5, 2, 18], [3, 2, 3, 11, 14, 8, 16, 10, 8, 9], [6, 9, 19, 6, 9, 8, 16, 10, 8, 0], [17, 18, 1, 7, 20, 20, 16, 20, 10, 4], [10, 16, 10, 5, 13, 5, 7, 13, 14, 6], [0, 8, 7, 7, 18, 10, 0, 10, 13, 17], [19, 14, 9, 12, 11, 19, 19, 18, 19, 15], [20, 6, 6, 14, 10, 16, 7, 5, 2, 1], [17, 14, 8, 4, 20, 17, 11, 19, 12, 5], [12, 16, 7, 19, 20, 16, 3, 15, 0, 6], [15, 20, 3, 1, 4, 19, 17, 4, 15, 13], [3, 17, 4, 9, 6, 19, 2, 15, 1, 9], [7, 16, 11, 8, 7, 3, 2, 3, 19, 12], [15, 16, 11, 1, 14, 17, 14, 20, 18, 18]]'

if __name__ == "__main__":
    data = eval(raw_data)
    kmeans = Kmeans(data, 3)
    kmeans.get_k_rand()
    kmeans.compare_to_k()
    kmeans.get_k_avarage()
    kmeans.compare_to_k2()


        
