from django.db import models
from datetime import datetime
from django.conf import settings

from django.dispatch import receiver
# from django.db.models.signals import post_deletenote

# Create your models here.

class AccountUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    phoneNumber = models.CharField(max_length=20)
    semester = models.CharField(max_length=10,default='1st')
    # s -> Student
    # P -> Prof

    def __str__(self):
        return self.user.username

class Professor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    phoneNumber = models.CharField(max_length=20)
    def __str__(self):
        return self.user.username

class Subject(models.Model):
    Sname = models.CharField(max_length=30)
    Sprof = models.ForeignKey(Professor,on_delete=models.CASCADE)
    Scredit = models.CharField(max_length=2)
    Ssemester = models.CharField(max_length=10)

    def __str__(self):
        return self.Sname

class Question(models.Model):
    QName = models.CharField(max_length=40)
    QCode = models.CharField(max_length=10)
    QDesc = models.TextField()
    createdBy = models.ForeignKey(Professor,on_delete=models.CASCADE)
    Qsubject = models.ForeignKey(Subject,default=1,on_delete=models.CASCADE)
    createdAt = models.DateTimeField(default=datetime.now, blank=True)
    testcases = models.IntegerField(default=0)
    def __str__(self):
        return self.QName



class Testcase(models.Model):
    Question = models.ForeignKey(Question,on_delete=models.CASCADE)
    input = models.FileField(upload_to='input')
    output = models.FileField(upload_to='output')
    def __str__(self):
        return self.Question.QName

# @receiver(post_delete, sender=Testcase)
# def submission_delete(sender, instance, **kwargs):
#     instance.file.delete(False) 

class Answers(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    result = models.CharField(max_length=100,default='0')
    code = models.FileField(upload_to='submit')
    submitedBy = models.ForeignKey(AccountUser,on_delete=models.CASCADE)
    submitedAt = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.question.Qname

