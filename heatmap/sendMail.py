import smtplib
from email.message import EmailMessage
import getpass
password = getpass.getpass('Password: ')

message = EmailMessage()
message['Subject'] = '이메일 제목'
message['From'] = 'wlsdh1110@naver.com' # 송신자 이메일
message['To'] = 'wlsdh1110@gmail.com' # 수신자 이메일 다수 (구분자: 콤마)

message.set_content('''이메일 내용
Test message
감사합니다. ;)''')
with smtplib.SMTP_SSL('smtp.naver.com', 465) as server:
	server.ehlo()
	server.login('wlsdh1110', password)
	server.send_message(message)

print('이메일 발송 성공')