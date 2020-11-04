
from django.shortcuts import render,redirect
from django.http import HttpResponse
#from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import login as auth_login, authenticate
from django.core import serializers
from .models import PeopleCount
from .models import Camera
from .models import Camtime
from operator import itemgetter
import json
import subprocess
import os
# Create your views here.
def ex(request):
#	command="python /var/www/html/ahyun2/people/PeopleCounter.py"
#	subprocess.call(command,shell=True)

	return redirect('home')
# 메인화면
def index(request):	
    return render(request, 'pages/index.html')

# 로그인
def login(request):
	if request.COOKIES.get('username') is not None:
		username=request.COOKIES.get('username')
		password=request.COOKIES.get('password')
		user=authenticate(username=username,password=password)
		if user is not None:
			auth_login(request,user)
			return render(request,'pages/index.html')
		else:
			return render(request,'registration/login.html')
	elif request.method == "POST":
		username=request.POST.get("username")
		password=request.POST.get("password")
		user=authenticate(username=username, password=password)
		if user:
			print("인증성공")
			auth_login(request,user)
			return render(request, 'pages/index.html')
		else:
			print("인증실패")
	return render(request, 'registration/login.html')

# 로그아웃
def logout(request):
	response=redirect('home')
	response.delete_cookie('username')
	response.delete_cookie('password')
	auth.logout(request)
	return response

# 피플 카운팅,히트맵
def report(request):
	name=request.user.username
	people=PeopleCount.objects.all()
	people=PeopleCount.objects.filter(username=name).order_by('-date')
	
	with open('/var/www/html/ahyun2/dldmsxor/8091/heatmap/heat.json') as json_file:
	    json_data = json.load(json_file)
	json_data.sort(key=itemgetter('value'),reverse=True)
	best=[]
	for i in range(0,3):
		best.append(json_data[i])
	worst=[]
	for i in range(24,21,-1):
		worst.append(json_data[i])
	print(best)
	print(worst)
	return render(request, 'pages/report.html',{'people_list':people,'best':best,'worst':worst})



# 회원가입
def register(request):
	if request.method=='POST':
		
		if request.POST.get("inputPassword")==request.POST.get("inputConfirmPassword"):
			name=request.POST.get("username")
			user=User.objects.create_user(
			username=request.POST.get("username"),email=request.POST.get("email"),
			password=request.POST.get("inputPassword"))
			user.last_name=request.POST.get("lastname")
			user.first_name=request.POST.get("firstname")
			
			user.save()
			address="/var/www/html/ahyun2/"+name
			try:
				if not os.path.exists(address):
					os.makedirs(address)
			except OSError:
				print('error')
			
			return redirect('home')
		return render(request,'register.html')
	return render(request,'register.html')

# 카메라 번호 등록
def camera(request):
	if request.method=='POST':		
		name=request.user.username
		cam_num=request.POST.get("cid")
		cam=Camera.objects.create(
		cid=request.POST.get("cid"),
		username=request.user.username)
		cam.save()
		address="/var/www/html/ahyun2/"+name+"/"+cam_num
		try:
			if not os.path.exists(address):
				os.makedirs(address)
		except OSError:
			print('error')

		message="등록완료"
		return render(request,'pages/camera_success.html',{'message':message})
	return render(rqeuest,'pages/index.html')
		
#피플카운팅 데이터 가져오기
def people(request):
	template_name='pages/examples.html'
	people_num=PeopleCount.objects.all()
	return render(request, template_name, {'people_num':people_num})


#카메라시간 세팅
def camSetting(request):
	return render(request,'pages/cam_settings.html')

#카메라시간 설정
def timeSetting(request):
	
	if request.method=='POST':
		time=Camtime.objects.create(
		username=request.user.username,
		detection_start=request.POST.get("detection_start"),
		detection_end=request.POST.get("detection_end"),
		peoplecount_start=request.POST.get("peoplecount_start"),
		peoplecount_end=request.POST.get("peoplecount_end"))
		time.save()
		message="설정 완료"
		return render(request,'pages/cam_settings_success.html',{'message':message})

#heatmap json

