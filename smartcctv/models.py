from django.db import models
#from django.contrib.auth.models import AbstractUser
# Create your models here.

#class User(AbstractUser():

class cctv(models.Model):
    user= models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    password=models.CharField(max_length=200)


class people(models.Model):
    cid=models.IntegerField(default=0)
    up=models.IntegerField(default=0)
    down=models.IntegerField(default=0)

class detect(models.Model):
	did=models.IntegerField(default=0)
	detect_at = models.DateTimeField(auto_now_add = True)

class heatmap(models.Model):
	hid=models.IntegerField(default=0)
	best=models.IntegerField(default=0)
	worst=models.IntegerField(default=0)


# 카메라 DB
class Camera(models.Model):
    cid = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'Camera'

#카메라 시간 DB
class Camtime(models.Model):
    username = models.CharField(primary_key=True, max_length=100)
    detection_start = models.IntegerField(blank=True, null=True)
    detection_end = models.IntegerField(blank=True, null=True)
    peoplecount_start = models.IntegerField(blank=True, null=True)
    peoplecount_end = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'camTime'

#피플카운팅 db
class PeopleCount(models.Model):
    username = models.CharField(max_length=45, blank=True, null=True)
    cid = models.IntegerField(blank=True, null=True)
    up = models.CharField(max_length=45, blank=True, null=True)
    down = models.CharField(max_length=45, blank=True, null=True)
    date = models.CharField(max_length=30, blank=True, null=True)
    
    def dic(self):
        fields=['username','cid','up','down','date']
        result={}
        for field in fields:
            result[field]=self.__dict__[field]
        return result

    class Meta:
        managed = False
        db_table = 'people_count'
	

