import argparse
import datetime
import time
import cv2
import numpy as np
import os
import smtplib
from email.message import EmailMessage
from email.mime.application import MIMEApplication


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

count = 0
mailcount = 0

if args.get("video", None) is None:

    #camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    #camera = cv2.VideoCapture('http://119.196.44.122:8091/?action=stream') # streaming video
    camera = cv2.VideoCapture('detecttest.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter('save2.avi', fourcc, 25.0, (640,480))

    time.sleep(0.25)
    camera.set(cv2.CAP_PROP_FPS,15)

else:
    camera = cv2.VideoCapture(args["video"])

firstFrame = None

while True:

    count = count + 1
    (grabbed, frame) = camera.read()
    text = "Unoccupied"

    if not grabbed:
        break

    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    fps = camera.get(cv2.CAP_PROP_FPS)
    #print(fps)

    if firstFrame is None:

        firstFrame = gray
        continue

    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    count2 = 0

    if (count % 3 == 0):

        for c in cnts:

            count2 = count2 + 1
            if cv2.contourArea(c) < args["min_area"]:
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            img_trim = frame[y:y + h, x:x + w]
            #cv2.imwrite("/home/pi/detect/pic/frame%d_%d.jpg" % (count, count2), img_trim)
            text = "Occupied"
            if text is "Occupied":
                #cv2.imwrite("C:/Users/wlsdh/Desktop/detectpic/frame%d_%d.jpg" % (count, count2), img_trim)
                cv2.imwrite("pic/frame%d_%d.jpg" % (count, count2), img_trim)
                out.write(frame)
                # print(count2)
                if mailcount == 0:
                    cv2.imwrite("pic/mail.jpg" , frame)
                    message = EmailMessage()
                    message['Subject'] = '이메일 제목'
                    message['From'] = 'wlsdh1110@naver.com'
                    message['To'] = 'cah0512@naver.com'

                    message.set_content('''침입이 감지되었습니다.''')
                    message.add_alternative('''
						<h1>침입이 탐지되었습니다.</h1>

                        <img src="cid:mail.jpg" />
                        <p> 침입이 탐지되었습니다. 사진을 확인해주세요.</p>
                        ''', subtype='html')
                    filepath_list = ['pic/mail.jpg']
                    for filepath in filepath_list:
                        with open(filepath, 'rb') as f:
                            filename = os.path.basename(filepath)
                            cid = filename
                            img_data = f.read()
                            part = MIMEApplication(img_data, name=filename)
                            if cid == 'mail.jpg':
                            	part.add_header('Content-ID', '<' + cid + '>')
                            else:
                             	part.add_header("Content-Disposition", "attachment; filename=\"%s\"" % filename)
                            message.attach(part)
                        with smtplib.SMTP_SSL('smtp.naver.com', 465) as server:
                            server.ehlo()
                            server.login('wlsdh1110', '')
                            server.send_message(message)

                        print('이메일 발송 성공')
                        mailcount = 1
                break
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    #cv2.imshow("Security Feed", frame)
    #cv2.imshow("Thresh", thresh)
    #cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
