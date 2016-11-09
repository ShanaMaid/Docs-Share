from django.shortcuts import render
from .models import Article,Usertable,Usergroup,Roletable
from django.http import JsonResponse
import time
from django.contrib.sessions.models import Session
# Create your views here.
def index(request):
	 content=Article.objects.filter(a_issee=True)
	 return render(request,'fontpage/index.html',{'content':content})
	#return render(request,'fontpage/index2.html')

def adminIndex(request):
	if bool(request.session['u_account']):
		return render(request,'fontpage/index.html',{'account':u_account})
	else:
		return render(request,'fontpage/login.html')

def deleteArticle(request):
	result={}
	if request.is_ajax():
		a_id=request.POST.get('article_id')
		u_account=request.POST.get('u_account')
		try:
			det_article=Article.objects.get(a_id=a_id)
			mod_user=Usertable.objects.get(u_account=u_account)
			det_score=mod_user.u_socre
			mod_user.u_socre=det_score-10
			det_article.delete()
			mod_user.save()
			result['ret_code']=0
			result['ret_msg']=''
		except Exception as e:
			result['ret_code']=-1
			result['ret_msg']=e
		finally:
			return JsonResponse(result)

def addArticle(request):
	result={}
	if request.method=='POST':
		a_title=request.POST.get('a_title')
		a_url=request.POST.get('a_url')
		a_type=request.POST.get('a_type')
		a_time=time.asctime(time.localtime(time.time()))
		a_reading_amount=0
		a_account=request.POST.get('a_account')
		a_isSee=false
		try:
			a_User=Usertable.objects.get(u_account=a_account)
			new_article=Article(a_User,a_title,a_url,a_type,a_title,a_reading_amount)
			new_article.save()
		except Exception as e:
			raise e
		finally:
			adminIndex(request)

def login(request):
	if request.method=='POST':
		u_account=request.POST.get('u_account')
		u_password=request.POST.get('u_password')
		try:
			checkUser=Usertable.objects.get(u_account=u_account,u_password=u_password)
			request.session['u_account']=u_account
			return render(request,'fontpage/index.html',{'account':u_account})
		except Exception as e:
			return render(request,'fontpage/login.html',{'error':'error','account':u_account,'password':u_password})
	if request.method=='GET':
		return render(request,'fontpage/login.html')

def logout(request):
	del request.session['u_account']
	adminIndex()

def approve(request):
	result={}
	if request.is_ajax():
		a_title=request.POST.get('a_title')
		try:
			approve_article=Article.object.get(a_title=a_title)
			approve_article.isSee=true
			approve.save()
			provider=Usertable.objects.filter(article__a_title=a_title)
			for single in provider:
				single.u_socre=single.u_socre+10
				single.save()
			result['ret_code']=0
			result['ret_msg']=''
		except Exception as e:
			result['ret_code']=0
			result['ret_msg']=e
		finally:
			return JsonResponse(result)

def addUser(request):
	if request.method=='POST':
		new_account=request.POST.get('u_account')
		new_password=request.POST.get('u_password')
		new_nickname=request.POST.get('u_nickname')
		new_score=0
		new_role=request.POST.get('u_role')
		new_group=request.POST.get('u_group')
		try:
			u_group=Usergroup.objects.get(g_name=new_group)
			u_role=Roletable.objects.get(r_type=new_role)
			Usertable(u_group,u_role,u_account,u_password,u_nickname,u_socre).save()
		except Exception as e:
			raise e
		finally:
			adminIndex(request)

def removeUser(request):
	result={}
	if request.is_ajax():
		u_account=request.POST.get('u_account')
		try:
			re_user=Usergroup.objects.get(u_account=u_account)
			re_user.delete()
			result['ret_code']=0
			result['ret_msg']=''
		except Exception as e:
			result['ret_code']=0
			result['ret_msg']=e
		finally:
			return JsonResponse(result)

def addGroup(request):
	 if request.method=='POST':
	 	group_title=request.POST.get('g_name')
	 	try:
	 		Usergroup.objects.get(g_name=group_title)
	 	except Exception as e:
	 		Usergroup(group_title).save()
	 		adminIndex(request)

def removeGroup(request):
	result={}
	if request.is_ajax():
		group_title=request.POST.get('g_name')
		try:
			re_group=Usergroup.objects.get(g_name=g_name)
			if re_group.sumperson!=0:
				result['ret_code']=-2
				result['ret_msg']='can not delete'
			else:
				re_group.delete()
				result['ret_code']=0
				result['ret_msg']=''
		except Exception as e:
			result['ret_code']=0
			result['ret_msg']=e
		finally:
			return JsonResponse(result)

def getGroup(request):
	group_result=Usergroup.objects.all()
	return group_result;

def checkRole(request,u_account):
	try:
		role=Roletable.objects.get(usertable__u_account=u_account)
		return role.r_type
	except Exception as e:
		return e

		
		