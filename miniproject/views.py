from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model, logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, JsonResponse

import os
import requests
from django.conf import settings

from .models import Answers, Question, AccountUser, Document, Subject, Testcase
from .forms import UploadFileForm


# Create your views here.

# file_ = open(os.path.join(settings.BASE_DIR,'filename'))


# def run(request):
# 	return render(request, 'run.html', {})


# def compile(request):
# 	# if request.method=='POST':
# 	if request.is_ajax():
# 		source = request.POST['source']
# 		lang = request.POST['lang']
# 		data = {
# 			'client_secret': 'efee14e3d19da585f2660381d79d81891f3417a9' ,
# 			'async': 0,
# 			'source': source,
# 			'lang': lang,
# 			'time_limit': 5,
# 			'memory_limit': 262144,
# 		}
# 		if 'input' in request.POST:
# 			data['input'] = request.POST['input']
# 		r = requests.post(RUN_URL, data=data)
# 		return JsonResponse(r.json(), safe=False)

# 	else:
# 		return HttpResponseForbidden()


def index(request):
	if not request.user.is_authenticated:
		return redirect('/loginuser')
	else:
		current_user = request.user
		print(current_user)
		subjects = Subject.objects.filter()
		# print(questions[0].QName)
		context = {
			'subjects':subjects,
			'user':True,
			'username': current_user.username
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
			'subject_id': subject_id
		}
		return render(request,'subject.html',context)
def question(request,subject_id,question_id):
	if request.method == 'POST':
		return
	else:
		question = Question.objects.get(id=question_id)
		testcase = Testcase.objects.filter(Question=question)
		print(testcase[0])

		context = {
			'subject_id': subject_id,
			'question' : question,
			'testcase':testcase
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
		return render(request,'newQuestion.html')

def viewfile(request,filename):
	with open('media/'+str(filename), 'r') as destination:
		stream = ""
		for chunk in destination.read():
			stream += chunk
		return HttpResponse(stream,content_type='text/plain')

# def viewQuestion(request,question_id):
# 	if request.method=='POST':
# 		pass
# 	else:
# 		question = Question.objects.filter(id=question_id)[0]
# 		# print(question)
# 		testCase = Document.objects.filter(Question=question)
# 		context = {
# 			'subject_id':subject_id
# 			'question':question,
# 			'cases':testCase
# 		}
# 		return render(request,'viewQuestion.html',context)

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
			'question_id':question_id
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
	return redirect('/')
