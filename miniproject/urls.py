from django.urls import path
from django.conf.urls.static import static

from . import views

app_name = 'miniproject'
urlpatterns = [
	path('',views.index,name='index'),
	path('signupuser',views.signup_view,name='signupuser'),
	path('loginuser',views.login_view,name='loginuser'),
	path('logoutuser',views.logout_view,name='logoutuser'),

	# view all question related toa subject
	path('s/<int:subject_id>',views.subject,name='subject'),
	# view a specific question
	path('s/<int:subject_id>/q/<int:question_id>',views.question,name='question'),


	path('s/<int:subject_id>/q/new',views.newQuestion,name='newQuestion'),
	path('s/<int:subject_id>/q/<int:question_id>/testcase/',views.testCase,name='testcase'),

	# path('question/<int:question_id>/add_testcase',views.addTestCase,name='addTestCase'),
	
	# path('question/<int:question_id>',views.viewQuestion,name='viewQuestion'),

	path('upload',views.upload,name='upload'),

	path('media/<str:filename>',views.viewfile,name='upload')

	# path('run',views.run,name='run'),
	# path('compile',views.compile,name='compile'),


	# path('add',views.add,name="add"),
	# path('details/<int:todo_id>',views.details,name="details"),
	# path('edit/<int:todo_id>',views.edit,name="edit"),
	# path('delete/<int:todo_id>',views.delete,name="delete")
]