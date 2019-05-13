from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model, logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, JsonResponse


import os
import requests, json
from django.conf import settings

from .models import Answers, Question, AccountUser, Subject, Testcase, Professor
from .forms import UploadFileForm


RUN_URL = 'https://api.jdoodle.com/v1/execute'

CLIENT_SECRET = '5db3f1c12c59caa1002d1cb5757e72c96d969a1a'



def index(request):
	if not request.user.is_authenticated:
		return redirect('/loginuser')
	else:
		subjects = Subject.objects.filter()
		# print(questions[0].QName)
		try:
			user = AccountUser.objects.get(user=request.user)
			userType = 'S'
		except:
			userType = 'P'

		context = {
			'subjects':subjects,
			'user':True,
			'userType':userType,
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
		try:
			user = AccountUser.objects.get(user=request.user)
			userType = 'S'
		except:
			userType = 'P'
		context = {
			'questions' : questions,
			'subject_id': subject_id,
			'userType':userType,
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
			input = testcase.input.read()
			# input = input.relpace('\r','')
			input = input.decode('unicode_escape')
			expectedOutput = testcase.output.read()
			# expectedOutput = expectedOutput.relpace('\r','')
			print(expectedOutput)
			expectedOutput = expectedOutput.decode('unicode_escape')
			print("INPUT")
			print(input)
			print("OUTPUT")
			print(expectedOutput)
			data = {
			    "script": source_code,
			    "stdin":input,
			    "language": "python3",
			    "versionIndex": "0",
			    "clientId": "d0b2ab4f943ca044aa8e9ee39290afd5",
			    "clientSecret":"8ddec190c616ac0aafdef83aa83e4a7a493c1415c44b81e29d49405ad5031dd"
			}
			output = requests.post(RUN_URL, json=data).json()
			print(output)
			output = output["output"]
			print("EXPOUTPUT")
			print(output)
			print(type(output),type(expectedOutput))
			if output==expectedOutput:
				print("CORRECT")
			else:
				flag = False
				error = output
				print(flag,error)
				break
		context = {
			'answer':flag,
			'error':error,
			'subject_id':subject_id
		}
			# print(output["output"])

		return render(request,'answer.html',context)
	else:
		question = Question.objects.get(id=question_id)
		testcase = Testcase.objects.filter(Question=question)
		subject = Subject.objects.get(id=subject_id)
		try:
			user = AccountUser.objects.get(user=request.user)
			try:
				testcase = testcase[:1]
			except:
				testcase = []
			userType = 'S'
		except:
			userType = 'P'

		context = {
			'subject_id': subject_id,
			'subject_name':subject.Sname,
			'userType':userType,
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

		user = Professor.objects.get(user=request.user)

		question = Question(
			QName = qName,
			QCode = qCode,
			QDesc = qDesc,
			createdBy = user,
			Qsubject = subject
		)
		question.save()
		return redirect('/')
	else:
		context = {
			'username': request.user.username,
			'subject_id':subject_id
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

		return redirect('/')
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
		sem = request.POST['sem']
		# try:
		user = User.objects.create_user(
			username = username,
			email=email,
			password=password
		)
		accountUser = AccountUser(
			user = user,
			phoneNumber = phoneNumber,
			semester = sem
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
