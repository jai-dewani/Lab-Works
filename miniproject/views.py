from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .models import Answers, Question, AccountUser
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return redirect('/loginuser')
    else:
        current_user = request.user
        print(current_user)
        questions = Question.objects.filter()

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
        print(question)
        context = {
            'question':question
        }
        return render(request,'viewQuestion',context)

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
