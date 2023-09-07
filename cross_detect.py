import sensor
import image
import time
import random
import math

class DSU():
    def __init__(self,num):
        father=[i for i in range(num)]
        size=[1 for i in range(num)]
        total=num
    def find_father(self,v):
        if father[v] != v :
            return father[v] = self.find_father(father[v])
        else
            return v
    def merge(self,x,y):
        if check(x,y)：
            return None
        xx=self.find_father(x)
        yy=self.find_father(y)
        if size[xx]>size[yy]:
            xx,yy=yy,xx
        father[xx]=yy
        size[yy]+=size[xx]
        total-=1
    def check(self,x,y):
        xx=self.find_father(x)
        yy=self.find_father(y)
        if father[x] == father[y]:
            return True
        else
            return False


def getEuclideanDistance(a,b):
    dx=a[0]-b[0]
    dy=a[1]-b[1]
    return (dx*dx+dy*dy)**0.5

def getManhattanDistance(a,b):
    dx=a[0]-b[0]
    dy=a[1]-b[1]
    return abs(dx)+abs(dy)

def quick_sort(arr, compare_func=None):
    if len(arr) <= 1:
        return arr

    pivot = random.choice(arr)  # 随机选择枢轴
    smaller, equal, larger = [], [], []

    for element in arr:
        if compare_func:
            comparison = compare_func(element, pivot)
        else:
            comparison = element - pivot

        if comparison < 0:
            smaller.append(element)
        elif comparison == 0:
            equal.append(element)
        else:
            larger.append(element)

    return quick_sort(smaller, compare_func) + equal + quick_sort(larger, compare_func)




sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)  # 设置图像为RGB565
sensor.set_framesize(sensor.QVGA)  # 设置图像分辨率为QVGA (320x240)
sensor.skip_frames(time=2000)  # 等待摄像头稳定

min_degree = 0
max_degree = 179

clock = time.clock() # Tracks FPS.

while True:
    clock.tick()
    img = sensor.snapshot()
    img.binary([(137, 255)])
    img.erode(3)
    img.dilate(5)
    img.find_edges(image.EDGE_CANNY, threshold=(50, 80))

    lines = img.find_lines(threshold = 1000, x_stride = 3, y_stride = 3, theta_margin = 25, rho_margin = 25)
    rhos = [i.rho() for i in lines]
    thetas = [i.theta() for i in lines]

    dsu=DSU(lines.size())
    for i in range(lines.size()):
        for j in range(lines.size()):
            if not dsu.check(i,j):
                if getEuclideanDistance([rhos[i],thetas[i]],[rhos[j],thetas[j]])<1:
                    dsu.merge(i,j)

    tags=[False for i in range(lines.size())]
    sets=[]
    for i in range(lines.size()):
        if tags[dsu.find_father(i)] == True :
            continue
        sets.append([dsu.find_father(i),dsu.size[dsu.find_father[i]]])

    quick_sort(sets,compare_func = lambda a, b: b[1] - a[1])
    if sets.size()<4:
        pass
    else:
        four_large_set = [ sets[i] for i in range(4) ]
        four_lines_set = []
        cnt = -1
        for i in four_large_set:
            cnt += 1
            for j in range(lines.size()):
                if dsu.find_father(j)==i[0]:
                    four_line_set[cnt].append([rhos[j],thetas[j]])
        cnt = -1
        avg_lines = []
        for i in four_line_set:
            cnt += 1
            avg_rho=sum([i[j][0] for j in range(len(i))])/len(i)
            avg_theta=sum([i[j][1] for j in range(len(i))])/len(i)
            avg_lines.append()
        # TODO
        # 生成一般式，所有边缘点匹配四条直线，
        # 然后对边缘的点做线性回归得四条构成十字的直线
        # 由此得到十字的直线解析式，据此计算十字中心

    print(clock.fps())