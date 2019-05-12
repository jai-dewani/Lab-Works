from django.contrib import admin

# Register your models here.

from .models import Answers,Question,AccountUser, Subject, Professor, Testcase
# from .forms import DocumentForm

admin.site.register(AccountUser)
admin.site.register(Professor)
admin.site.register(Subject)
admin.site.register(Question)
admin.site.register(Testcase)
admin.site.register(Answers)
