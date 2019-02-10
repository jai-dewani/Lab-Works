from django.contrib import admin

# Register your models here.

from .models import Answers,Question,AccountUser
admin.site.register(Answers)
admin.site.register(Question)
admin.site.register(AccountUser)
