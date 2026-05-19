from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Student(models.Model):
    name=models.CharField(max_length=100)
    dob=models.DateField()
    college=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    department=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    pincode=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    photo=models.CharField(max_length=500)
    USER=models.OneToOneField(User,on_delete=models.CASCADE)

class EventOrganaizer(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    gender=models.CharField(max_length=100,default='')
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    photo=models.CharField(max_length=500)
    USER=models.OneToOneField(User,on_delete=models.CASCADE)


class refree(models.Model):
    name = models.CharField(max_length=100, default='')
    gender = models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='')
    mobile = models.CharField(max_length=100, default='')
class EventCategory(models.Model):
    name=models.CharField(max_length=100,default='')

class Poster(models.Model):
    photo=models.CharField(max_length=500,default='')
    title=models.CharField(max_length=100,default='')
    EVENTORGANIZER= models.ForeignKey(EventOrganaizer,on_delete=models.CASCADE,default='')

class SportsEvent(models.Model):
    name=models.CharField(max_length=100)
    # shedule=models.CharField(max_length=300)
    # description=models.CharField(max_length=100)
    eventtype=models.CharField(max_length=100)
    photo=models.CharField(max_length=100)
    date=models.DateField()
    status=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    REFREE=models.ForeignKey(refree,on_delete=models.CASCADE,default='')
    EVENTORGANAIZER=models.ForeignKey(EventOrganaizer,on_delete=models.CASCADE)

class shedule(models.Model):
    description=models.CharField(max_length=200,default='')
    date=models.DateField(default='')
    fromTime=models.TimeField(default='')
    toTime=models.TimeField(default='')
    EVENT=models.ForeignKey(SportsEvent,on_delete=models.CASCADE,default='')
    ORGANAIZER=models.ForeignKey(EventOrganaizer,on_delete=models.CASCADE,default='')
class Register(models.Model):
    date=models.DateField()
    status=models.CharField(max_length=100)
    STUDENT=models.ForeignKey(Student,on_delete=models.CASCADE,default='')
    EVENT=models.ForeignKey(SportsEvent,on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to="qrcodes/", blank=True, null=True)
    winner=models.CharField(max_length=100,default='')
class Review(models.Model):
    date=models.DateField()
    review=models.CharField(max_length=100)
    positive=models.IntegerField(default='0')
    negative=models.IntegerField(default='0')
    nutrel=models.IntegerField(default='0')
    STUDENT=models.ForeignKey(Student,on_delete=models.CASCADE)
    EVENT = models.ForeignKey(SportsEvent, on_delete=models.CASCADE, default='')
class Complaint(models.Model):
    date=models.DateField()
    complaint=models.CharField(max_length=100)
    replay=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    STUDENT=models.ForeignKey(Student,on_delete=models.CASCADE)


