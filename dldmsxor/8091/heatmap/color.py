import numpy as np
import cv2
#from sklearn.cluster import KMeans
#import matplotlib.pyplot as plt
import json
from io import StringIO
est = list()

for i in range(1, 26):
    # print("------------%d번 구역-----------" %(i))
    image = cv2.imread("pic/%d.jpg" % (i))
    # image = cv2.imread("C:/Users/wlsdh/Desktop/pic/%d.jpg" % (i))
    # print(image.shape)
    # (96, 128, 3)
    # 채널을 BGR -> RGB로 변경
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    avg_color_per_row = np.average(image, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    # print(avg_color)
    result = avg_color[0]*5 # + avg_color[1]*2
    with open('heat.json', mode='w', encoding='utf-8') as f:
        json.dump([], f)
    with open('heat.json', mode='w', encoding='utf-8') as feedsjson:
        entry = {'section': i, 'value': result}
        est.append(entry)
        json.dump(est, feedsjson, indent="\t")
