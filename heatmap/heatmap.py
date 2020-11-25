import numpy as np
import cv2
from PIL import ImageFont, ImageDraw, Image
import time
import argparse
import json

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())
#print("test cron")
count =0
if args.get("video", None) is None:

    #camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    #camera = cv2.VideoCapture('http://ipaddress:port/?action=stream') # streaming video
    cap = cv2.VideoCapture('Heattest88.avi')
    time.sleep(0.25)
    cap.set(cv2.CAP_PROP_FPS,15)

else:
    cap = cv2.VideoCapture(args["video"])

firstFrame = None

# frame size
h = 480
w = 640
frameArea = h * w

# line
line_up = int(2.0 * (h / 5))
line_down = int(3.0 * (h / 5))

up_limit = int(1.0 * (h / 5))
down_limit = int(4.0 * (h / 5))

line_up2 = int(2.0 * (w / 5))
line_down2 = int(3.0 * (w / 5))

up_limit2 = int(1.0 * (w / 5))
down_limit2 = int(4.0 * (w / 5))

pt1 = [0, line_down];
pt2 = [w, line_down];
pts_L1 = np.array([pt1, pt2], np.int32)
pts_L1 = pts_L1.reshape((-1, 1, 2))
pt3 = [0, line_up];
pt4 = [w, line_up];
pts_L2 = np.array([pt3, pt4], np.int32)
pts_L2 = pts_L2.reshape((-1, 1, 2))

pt5 = [0, up_limit];
pt6 = [w, up_limit];
pts_L3 = np.array([pt5, pt6], np.int32)
pts_L3 = pts_L3.reshape((-1, 1, 2))
pt7 = [0, down_limit];
pt8 = [w, down_limit];
pts_L4 = np.array([pt7, pt8], np.int32)
pts_L4 = pts_L4.reshape((-1, 1, 2))

pt9 = [line_down2, 0];
pt10 = [line_down2, h];
pts_L5 = np.array([pt9, pt10], np.int32)
pts_L5 = pts_L5.reshape((-1, 1, 2))
pt11 = [line_up2, 0];
pt12 = [line_up2, h];
pts_L6 = np.array([pt11, pt12], np.int32)
pts_L6 = pts_L6.reshape((-1, 1, 2))

pt13 = [up_limit2, 0];
pt14 = [up_limit2, h];
pts_L7 = np.array([pt13, pt14], np.int32)
pts_L7 = pts_L7.reshape((-1, 1, 2))
pt15 = [down_limit2, 0];
pt16 = [down_limit2, h];
pts_L8 = np.array([pt15, pt16], np.int32)
pts_L8 = pts_L8.reshape((-1, 1, 2))


while True:
    try:
        _, f = cap.read()
        f = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) # convert black white
        f = cv2.GaussianBlur(f, (11, 11), 2, 2)
        cnt = 0
        res = 0.05 * f
        res = res.astype(np.float64)
        break
    except:
        print('s')

fgbg = cv2.createBackgroundSubtractorMOG2(history=1, varThreshold=100,
                                          detectShadows=True)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13)) # create kernel matrix
cnt = 0
while True:
    cnt += 1
    ret, frame = cap.read()
    if not ret: break
    fgmask = fgbg.apply(frame, None, 0.01)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (11, 11), 2, 2)
    gray = gray.astype(np.float64)
    fps= cap.get(cv2.CAP_PROP_FPS)

    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    fgmask = fgmask.astype(np.float64)
    res += (40 * fgmask + gray) * 0.01
    res_show = res / res.max()
    res_show = np.floor(res_show * 255) 
    res_show = res_show.astype(np.uint8)
    res_show = cv2.applyColorMap(res_show, cv2.COLORMAP_JET) # convert video color
    img = res_show
    #line
    res_show = cv2.polylines(res_show, [pts_L1], False, (255, 255, 255), thickness=2)
    res_show = cv2.polylines(res_show, [pts_L2], False, (255, 255, 255), thickness=2)
    res_show = cv2.polylines(res_show, [pts_L3], False, (255, 255, 255), thickness=2)
    res_show = cv2.polylines(res_show, [pts_L4], False, (255, 255, 255), thickness=2)
    res_show = cv2.polylines(res_show, [pts_L5], False, (255, 255, 255), thickness=2)
    res_show = cv2.polylines(res_show, [pts_L6], False, (255, 255, 255), thickness=2)
    res_show = cv2.polylines(res_show, [pts_L7], False, (255, 255, 255), thickness=2)
    res_show = cv2.polylines(res_show, [pts_L8], False, (255, 255, 255), thickness=2)
    b, g, r, a = 255, 255, 255, 0
    res_show = Image.fromarray(res_show)
    res_show = np.array(res_show)

    i = 0
    for a in range(0, 5):
        for b in range(0, 5):
            cv2.putText(res_show, "%d" %(i+1) , (50+(b*128), 55+(a*96)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)
            i+= 1
    cv2.IMREAD_UNCHANGED
    cv2.imwrite("/var/www/html/ahyun2/smartcctv/static/img/test.jpg", res_show)
    # img = cv2.imread('/var/www/html/ahyun2/smartcctv/static/img/test.jpg')
    # cv2.imwrite("C:/Users/wlsdh/Desktop/pic/test.jpg", res_show)
    # img = cv2.imread('C:/Users/wlsdh/Desktop/pic/test.jpg')
    i = 1
    for height in range(0, 5):
        for width in range(0, 5):
            y1 = int((height * h / 5))
            y2 = int(((height + 1) * h / 5))
            x1 = int(width * (w / 5))
            x2 = int(((width + 1) * w / 5))
            res_img = img[y1: y2, x1: x2]
            test = str(i)
            cv2.imwrite("pic/%d.jpg" % (i), res_img)
            # cv2.imwrite("C:/Users/wlsdh/Desktop/pic/%d.jpg" % (i), res_img)
            #cv2.imshow(test, res_img)
            i += 1
    k = cv2.waitKey(30) & 0xff
    
cap.release()
cv2.destroyAllWindows()

est = list()

for i in range(1, 26):
    image = cv2.imread("pic/%d.jpg" % (i))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    avg_color_per_row = np.average(image, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    result = avg_color[0]*5 # + avg_color[1]*2
    with open('/var/www/html/ahyun2/dldmsxor/8091/heatmap/heat.json', mode='w', encoding='utf-8') as f:
        json.dump([], f)
    with open('/var/www/html/ahyun2/dldmsxor/8091/heatmap/heat.json', mode='w', encoding='utf-8') as feedsjson:
        entry = {'section': i, 'value': result}
        est.append(entry)
        json.dump(est, feedsjson, indent="\t")

