from django.db import models
from datetime import datetime
from django.conf import settings
# Create your models here.

class AccountUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    phoneNumber = models.CharField(max_length=20)
    accountType = models.CharField(max_length=30)
    def __str__(self):
        return self.user.username

class Question(models.Model):
    QName = models.CharField(max_length=40)
    QCode = models.CharField(max_length=10)
    QDesc = models.TextField()
    createdBy = models.ForeignKey(AccountUser,on_delete=models.CASCADE)
    created = models.DateTimeField(default=datetime.now(), blank=True)
    def __str__(self):
        return self.QName

class TestCase(models.Model):
    Question = models.ForeignKey(Question,on_delete=models.CASCADE)
    input = models.TextField()
    output = models.TextField()


class Answers(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    code = models.TextField()
    submitedBy = models.ForeignKey(AccountUser,on_delete=models.CASCADE)
    created = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.question
