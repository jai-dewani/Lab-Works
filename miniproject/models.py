from django.db import models
from datetime import datetime
from django.conf import settings
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

    def __str__(self):
        return self.QName

# class TestCase(models.Model):
#     Question = models.ForeignKey(Question,on_delete=models.CASCADE)
#     input = models.TextField()
#     output = models.TextField()


class Answers(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    code = models.TextField()
    submitedBy = models.ForeignKey(AccountUser,on_delete=models.CASCADE)
    submitedAt = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.question

class Document(models.Model):
    # document = models.FileField(upload_to='document/')
    Question = models.ForeignKey(Question,on_delete=models.CASCADE)
    input = models.CharField(max_length=255, blank=True)
    output = models.CharField(max_length=255, blank=True)
    upload_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description