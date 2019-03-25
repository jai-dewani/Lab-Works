from django.contrib import admin

# Register your models here.

from .models import Answers,Question,AccountUser, Document
from .forms import DocumentForm
admin.site.register(Answers)
admin.site.register(Question)
admin.site.register(AccountUser)
admin.site.register(Document)
