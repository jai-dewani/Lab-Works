from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model, logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, JsonResponse


import os
import requests, json
from django.conf import settings

from .models import Answers, Question, AccountUser, Subject, Testcase
from .forms import UploadFileForm


RUN_URL = 'https://api.jdoodle.com/v1/execute'

CLIENT_SECRET = '5db3f1c12c59caa1002d1cb5757e72c96d969a1a'



def index(request):
	if not request.user.is_authenticated:
		return redirect('/loginuser')
	else:
		subjects = Subject.objects.filter()
		# print(questions[0].QName)
		context = {
			'subjects':subjects,
			'user':True,
			'username': request.user.username
		}
		print(context)

		return render(request,'index.html',context)

def subject(request,subject_id):
	if request.method == 'POST':
		return 

	else:
		subject = Subject.objects.get(id=subject_id)
		questions = Question.objects.filter(Qsubject=subject)
		context = {
			'questions' : questions,
			'subject_id': subject_id,
			'username': request.user.username
		}
		return render(request,'subject.html',context)
def question(request,subject_id,question_id):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		source_code = request.FILES['code'].read().decode('unicode_escape')
		# print(source_code)
		question = Question.objects.get(id=question_id)
		testcases = Testcase.objects.filter(Question=question)
		flag = True,
		error = ''
		for testcase in testcases:
			input = testcase.input.read().decode('unicode_escape')
			expectedOutput = testcase.output.read().decode('unicode_escape')
			data = {
			    "script": source_code,
			    "stdin":input,
			    "language": "python3",
			    "versionIndex": "0",
			    "clientId": "d0b2ab4f943ca044aa8e9ee39290afd5",
			    "clientSecret":"8ddec190c616ac0aafdef83aa83e4a7a493c1415c44b81e29d49405ad5031dd"
			}
			r = requests.post(RUN_URL, json=data).json()
			output = output["output"]
			if output!=expectedOutput:
				flag = False
				error = output
				break
		context = {
			'answer':flag,
			'error':error
		}
			# print(output["output"])

		return redirect('/')
	else:
		question = Question.objects.get(id=question_id)
		testcase = Testcase.objects.filter(Question=question)

		context = {
			'subject_id': subject_id,
			'question' : question,
			'testcase':testcase,
			'username': request.user.username
		}
		return render(request,'viewQuestion.html',context)

def newQuestion(request,subject_id):
	if request.method=='POST':
		qName = request.POST['questionName']
		qCode = request.POST['questionCode']
		qDesc = request.POST['questionDesc']
		print(request.user)
		subject = Subject.objects.get(id=subject_id)
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
		context = {
			'username': request.user.username
		}
		
		return render(request,'newQuestion.html',context)

def viewfile(request,filename):
	with open('media/'+str(filename), 'r') as destination:
		stream = ""
		for chunk in destination.read():
			stream += chunk
		return HttpResponse(stream,content_type='text/plain')

def testCase(request,subject_id,question_id):
	if request.method=='POST':
		form = UploadFileForm(request.POST, request.FILES)


		question = Question.objects.get(id=question_id)
		question.testcases += 1
		question.save()
		testcase = Testcase(Question=question,input=request.FILES['input'],output=request.FILES['output'])
		testcase.save()

		return redirect('/s/'+str(question_id))
	else:
		context = {
			'subject_id':subject_id,
			'question_id':question_id,
			'username': request.user.username
		}
		return render(request,'testcase.html',context)

def handle_uploaded_file(f,filename):
	print(filename)
	with open('media/'+str(filename), 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)

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
			'documents':documents,
			'username': request.user.username
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
		accountUser = AccountUser(
			user = user,
			phoneNumber = phoneNumber,
			accountType = str(accountType)
		)
		accountUser.save()
		user = authenticate(
			request,
			username=username,
			password=password
		)
		if user is not None:
			login(request,user)
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
	return redirect('/')
