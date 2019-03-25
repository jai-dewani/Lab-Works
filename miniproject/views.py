from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

import os
from django.conf import settings

from .models import Answers, Question, AccountUser, Document
from .forms import DocumentForm
# Create your views here.

# file_ = open(os.path.join(settings.BASE_DIR,'filename'))



def index(request):
    if not request.user.is_authenticated:
        return redirect('/loginuser')
    else:
        current_user = request.user
        print(current_user)
        questions = Question.objects.filter()
        # print(questions[0].QName)
        context = {
            'questions':questions,
            'user':True
        }

        return render(request,'index.html',context)

def newQuestion(request):
    if request.method=='POST':
        qName = request.POST['questionName']
        qCode = request.POST['questionCode']
        qDesc = request.POST['questionDesc']
        print(request.user)
        user = AccountUser.objects.filter(user=request.user)[0]
        print(user.phoneNumber) 

        question = Question(
            QName = qName,
            QCode = qCode,
            QDesc = qDesc,
            createdBy = user,
        )
        question.save()
        return redirect('question/'+str(question.id))
    else:
        return render(request,'newQuestion.html')

def viewQuestion(request,question_id):
    if request.method=='POST':
        pass
    else:
        question = Question.objects.filter(id=question_id)[0]
        # print(question)
        testCase = Document.objects.filter(Question=question)
        context = {
            'question':question,
            'cases':testCase
        }
        return render(request,'viewQuestion.html',context)

def addTestCase(request,question_id):
    if request.method=='POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        input = request.POST['input']
        output = request.POST['output']
        question = Question.objects.filter(id=question_id)[0]
        testcase = TestCase(
            Question = question,
            input = input,
            output = output
        )
        testcase.save()
        return redirect('question/'+str(question_id))
    else:
        return render(request,'addTestCase.html')

def upload(request):
    if request.method=='POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # return redirect('/')
    else:
        form = DocumentForm()
    documents = Document.objects.all()
    return render(request, 'upload.html',{
            'form':form,
            'documents':documents
        })

def signup_view(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        phoneNumber = request.POST['phoneNumber']
        accountType = request.POST['accountType']
        print(accountType)
        # try:
        user = User.objects.create_user(
            username = username,
            email=email,
            password=password
        )
        print(user)
        accountType = str(accountType)
        accountUser = AccountUser(
            user = user,
            phoneNumber = phoneNumber,
            accountType = accountType
        )
        accountUser.save()
        print(user)
        '''except:
            context= {
                'message':'This account can not be created.'
            }
            # print(message)
            return render(request,'signup.html',context)
        '''
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request,user)
            print(user)
            return redirect('/')
        else:
            print("PROBLEM")
            context = {
                'message': 'Check login credentials'
            }
            return render(request,'login.html',context)
    else:
        return render(request,'signup.html')


def login_view(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request,user)
            print(user)
            return redirect('/')
        else:
            print("PROBLEM")
            context = {
                'message': 'Check login credentials'
            }
            return render(request,'login.html',context)
    else:
        return render(request,'login.html')

def logout_view(request):
    logout(request)
    return('/')
