import random

def gen(childnum, days):
    data = []
    for i in range(childnum):
        astu = []
        for j in range(days):
            a = random.randint(0, 20)
            astu.append(a)
        data.append(astu)
    print(data)

if __name__ == '__main__':
    gen(20, 10)
