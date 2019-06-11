from django.shortcuts import render
from django.contrib.auth.decorators import login_required
#from posts.serializers import PostSerializer
from django.views import generic
from django.http import HttpResponse, JsonResponse
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings
from .models import Post, Courses, Subscribers

#@login_required

def index(request):
	"""
	Функция отображения для домашней страницы сайта.
	"""
	# Генерация "количеств" некоторых главных объектов
	posts=Post.objects.all().order_by('-modified_at')[:4]
	courses=Courses.objects.all().order_by('-modified_at')[:6]

	# Отрисовка HTML-шаблона index.html с данными внутри 
	# переменной контекста context
	return render(
		request,
		'index.html',
		context={'posts':posts, 'courses':courses},
	)

def about(request):
	return render(
		request,
		'about.html',
	)

def contact(request):
	return render(
		request,
		'contact.html',
	)

def success(request):
	email = request.POST.get('email', '')
	name = request.POST.get('name', '')
	subject = request.POST.get('subject', '')
	description = request.POST.get('description', '')
	id = request.POST.get('id', 'None')
	subscribeEmail = ""
	idCource = None
	random = ""
	confirmation = False
	myemail = 'radugaug@gmail.com'
	for validEmail in Subscribers.objects.values('email','courses', 'confirmation').filter(email=email,):
		subscribeEmail = validEmail['email']
		idCource = validEmail['courses']
		confirmation = validEmail['confirmation']
	if subscribeEmail == "" and idCource == None:
		random = get_random_string(length=10)
		subscribers = Subscribers.objects.create(email=email, randomkey = random)
		if id != None:
			subscribers.courses.add(id)
		subscribers.save()
		newurl = request.build_absolute_uri().rsplit(request.get_full_path(),1)[0]+'/posts/confirmation/'+email+'/'+random
		send_mail('Subscription confirmation', 'Hello!\nDear, '+name+'.\n For confirm your subscription, follow the link below.:\n'+newurl, None, [email], fail_silently=False)
		return render(request, 'success.html', context={'name':name},)
	elif subscribeEmail != "" and idCource == None:
		if Subscribers.objects.filter(email=email,).count() > 1:
			return render(request, 'nosuccess.html', context={'name':name},)
		subscribers = Subscribers.objects.get(email=email,)
		subscribers.courses.add(id)
		subscribers.save()
		send_mail(subject, 'The user '+name+' wants to sign up for the course with id '+id+'\n Message from user:\n'+description+'\n\nPreviously, the user was just a subscriber..', None, [myemail], fail_silently=False)
		return render(request, 'success.html', context={'name':name},)
	elif subscribeEmail != "" and idCource != None:
		subscribers = ""
		if int(idCource) == int(id) and subscribeEmail == email:
			return render(request, 'nosuccess.html', context={'name':name},)
		elif confirmation == True:
			subscribers = Subscribers.objects.create(email=email, randomkey = random, confirmation = True)
		else:
			subscribers = Subscribers.objects.create(email=email, randomkey = random)
		subscribers.courses.add(id)
		subscribers.save()
		send_mail(subject, 'The user '+name+' wants to sign up for the course with id '+id+'\n Message from user:\n'+description+'\n\nPreviously, the user was just a subscriber..', None, [myemail], fail_silently=False)
		return render(request, 'success.html', context={'name':name},)
	else:
		return render(request, 'nosuccess.html', context={'name':name},)

def confirmation(request, email = None, random = 1203):
	myemail = 'radugaug@gmail.com'
	try:
		subscribers = Subscribers.objects.get(email=email, randomkey=random)
	except Subscribers.DoesNotExist:
		return render(request, 'confirmation.html', context={'email':'Email '+email+' don\'t confirmation. Please, don\'t change link!'},)
	if str(subscribers.email) != str(email) or str(subscribers.randomkey) != str(random):
		return render(request, 'confirmation.html', context={'email':'Email '+email+' don\'t confirmation. Please, don\'t change link!'},)
	else:
		subscriber = Subscribers.objects.filter(email=email,)
		for subscribe in subscriber:
			subscribe.confirmation = True
			subscribe.save()
			send_mail('Confirmation', 'The user confirmate his e-mail: '+email, None, [myemail], fail_silently=False)
	return render(request, 'confirmation.html', context={'email':'Email '+email+' is confirmated'},)

def subscribe(request):
	email = request.POST.get('email', '')
	subscribeEmail = None
	for validEmail in Subscribers.objects.values('email',).filter(email=email,):
		subscribeEmail = validEmail['email']
	print(email, subscribeEmail)
	if subscribeEmail == None:
		random = get_random_string(length=10)
		subscribers = Subscribers(email=email, randomkey = random)
		subscribers.save()
		newurl = request.build_absolute_uri().rsplit(request.get_full_path(),1)[0]+'/posts/confirmation/'+email+'/'+random
		send_mail('Subscription confirmation', 'To confirm your mailbox subscription '+email+' go to the next link:\n'+newurl, None, [email], fail_silently=False)
		return JsonResponse('Mailbox subscription '+email+' has been send', safe=False)
	else:
		return JsonResponse('This email is already among the subscribers.', safe=False)

class Blog(generic.ListView):
	"""
	Класс отображения записей блога
	"""
	model = Post
	context_object_name = 'posts'
	template_name ='blog.html'
	paginate_by = 4

class BlogView(generic.DetailView):
	"""
	Класс отображения записи блога
	"""
	model = Post
	template_name ='single-blog.html'

class Coursess(generic.ListView):
	"""
	Класс отображения записей блога
	"""
	model = Courses
	context_object_name = 'courses'
	template_name ='course.html'
	paginate_by = 6

class CourseView(generic.DetailView):
	"""
	Класс отображения записи блога
	"""
	model = Courses
	template_name ='single-course.html'
