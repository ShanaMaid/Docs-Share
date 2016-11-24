from django.shortcuts import render
from .models import Article,Usertable,Usergroup,Roletable
from django.http import JsonResponse
import time
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers 
# Create your views here.
def index(request):
	 content=Article.objects.filter(a_issee=True)
	 return render(request,'fontpage/index.html',{'content':content})
	#return render(request,'fontpage/index2.html')

def adminIndex(request,message):
	if request.session.get('u_account',False):
		log_type=Roletable.objects.get(usertable__u_account=request.session['u_account'])
		if log_type.r_type=='manager':
			pageList=getSubmitPage()
			print 3
			personList=PersonList(log_type.r_type)
			return render(request,'fontpage/manager.html',{'account':request.session['u_account'],'message':message,'pageList':pageList,'personList':personList})
		elif log_type.r_type=='headman':
			personList=PersonList(log_type.r_type)
			return render(request,'fontpage/headman.html',{'account':request.session['u_account'],'message':message,'personList':personList})
		else:
			return render(request,'fontpage/member.html',{'account':request.session['u_account'],'message':message})
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
	else:
		 result['ret_code']=-2
		 result['ret_msg']="illegal"
		 return JsonResponse(result)
@csrf_exempt
def addArticle(request):
	result={}
	if request.method=='POST':
		a_title=request.POST.get('a_title')
		a_url=request.POST.get('a_url')
		a_type=request.POST.get('a_type')
		a_time=None
		a_reading_amount=0
		a_account=request.session['u_account']
		a_issee=False
		try:
			a_User=Usertable.objects.get(u_account=a_account)
			new_article=Article(u=a_User,a_title=a_title,a_url=a_url,a_type=a_type,a_time=a_time,a_reading_amount=a_reading_amount,a_issee=a_issee)
			new_article.save()
			result['ret_code']=0
			result['ret_msg']=''
		except Exception as e:
			result['ret_code']=-1
			result['ret_msg']=e
	else:
		result['ret_code']=-2
		result['ret_msg']="illegal"
	return JsonResponse(result)

def login(request):
	if request.session.get('u_account',False)!=True:
		if request.method=='POST':
			u_account=request.POST.get('u_account')
			u_password=request.POST.get('u_password')
			try:
				checkUser=Usertable.objects.get(u_account=u_account,u_password=u_password)
				request.session['u_account']=u_account
				result={}
				result['ret_code']=0
				result['ret_msg']=''
				return adminIndex(request,result)
			except Exception as e:
				return render(request,'fontpage/login.html',{'error':'error','account':u_account,'password':u_password})
		if request.method=='GET':
			return render(request,'fontpage/login.html',{'error':"ooo"})
	else:
		return render(request,'fontpage/login.html',{'error':"xxx"})

def logout(request):
		result={}
		if request.session.get('u_account',False):
			del request.session['u_account']
			result['ret_code']=0
			result['ret_msg']="logout"
			return render(request,'fontpage/index.html')
		else:
			return render(request,'fontpage/login.html')

def approve(request):
	result={}
	if request.is_ajax():
		a_title=request.POST.get('a_title')
		try:
			approve_article=Article.object.get(a_title=a_title)
			approve_article.a_issee=True
			approve.save()
			provider=Usertable.objects.filter(article__a_title=a_title)
			for single in provider:
				single.u_socre=single.u_socre+10
				single.save()
			result['ret_code']=0
			result['ret_msg']=''
		except Exception as e:
			result['ret_code']=-1
			result['ret_msg']=e
		finally:
			return JsonResponse(result)
	else:
		result['ret_code']=-2
		result['ret_msg']="illegal"
		return JsonResponse(result)

@csrf_exempt
def addUser(request):
	result={}
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
			Usertable(g=u_group,r=u_role,u_account=new_account,u_password=new_password,u_nickname=new_nickname,u_score=new_score).save()
			sumperson=u_group.sumperson
			u_group.sumperson=sumperson+1
			u_group.save()
			result['ret_code']=0
			result['ret_msg']=''
		except Exception as e:
			result['ret_code']=-1
			result['ret_msg']=e
	else:
		result['ret_code']=-2
		result['ret_msg']="illegal"
	return JsonResponse(result)

def removeUser(request):
	result={}
	if request.is_ajax():
		u_account=request.POST.get('u_account')
		try:
			re_user=Usergroup.objects.get(u_account=u_account)
			sumperson=Usergroup.objects.get(usertable__u_account=u_account).sumperson
			Usergroup.objects.get(usertable__u_account=u_account).sumperson=sumperson-1
			re_user.delete()
			result['ret_code']=0
			result['ret_msg']=''
		except Exception as e:
			result['ret_code']=-1
			result['ret_msg']=e
		finally:
			return JsonResponse(result)
	else:
		result['ret_code']=-2
		result['ret_msg']="illegal"
		return JsonResponse(result)

def addGroup(request):
	result={}
	if request.method=='POST':
	 	group_title=request.POST.get('g_name')
	 	try:
	 		Usergroup.objects.get(g_name=group_title)
	 		result['ret_code']=-3
			result['ret_msg']="Group already exist"
	 	except Exception as e:
	 		Usergroup(g_name=group_title).save()
	 		result['ret_code']=0
			result['ret_msg']=''
		finally:
	 		adminIndex(request,result)
	else:
	 	result['ret_code']=-2
		result['ret_msg']="illegal"
		adminIndex(request,result)

def removeGroup(request):
	result={}
	if request.is_ajax():
		group_title=request.POST.get('g_name')
		try:
			re_group=Usergroup.objects.get(g_name=g_name)
			if re_group.sumperson!=0:
				result['ret_code']=-4
				result['ret_msg']='can not delete'
			else:
				re_group.delete()
				result['ret_code']=0
				result['ret_msg']=''
		except Exception as e:
			result['ret_code']=-1
			result['ret_msg']=e
		finally:
			return JsonResponse(result)
	else:
		result['ret_code']=-2
		result['ret_msg']="illegal"
		return JsonResponse(result)

def getGroup(request):
	result={}
	group_result=Usergroup.objects.all()
	result['ret_code']=0
	result['group_result']=serializers.serialize("json", group_result)
	result['ret_msg']=''
	return JsonResponse(result);

def checkRole(request,u_account):
	result={}
	try:
		role=Roletable.objects.get(usertable__u_account=u_account)
		result['ret_code']=0
		result['r_type']=role.r_type
		result['ret_msg']=''
	except Exception as e:
		result['ret_code']=-1
		result['ret_msg']=e
	finally:
		return JsonResponse(result)
def clients(request):
	if 'u_account' in request.session:
		return render(request,'fontpage/clients.html',{"u_account":request.session['u_account']})
	else:
		return render(request,'fontpage/login.html')
		
def test(request):
	return render(request,'fontpage/test.html')
		

def getSubmitPage():
	result={}
	try:
		content=Article.objects.filter(a_issee=False)
		print any(content)
	except Exception as e:
		print e
	result['ret_code']=0
	JsonContent=serializers.serialize("json", content)
	result['content']=JsonContent
	result['ret_msg']=''
	print JsonResponse(result)
	return JsonResponse(result)
def getPersonInfo(request):
	result={}
	if request.method=='POST':
		u_account=request.POST.get("u_account");
		try:
			personInfo=Usertable.objects.get(u_account=u_account);
			result['ret_code']=0
			result['personInfo']=personInfo
			result['ret_msg']=''
		except Exception as e:
			result['ret_code']=-1
			result['ret_msg']=e
	else:
	 	pass
	return JsonResponse(result)
def PersonList(r_type):
	result={}
	if r_type=='manager':
		try:
			content=Usertable.objects.filter(r__r_type="headman")
			print any(content)
		except Exception as e:
			print e
	elif r_type=='headman':
		content=Usertable.objects.filter(r__r_type="member")
	result['ret_code']=0
	#result['content']=serializers.serialize("json", content)
	result['ret_msg']=''
	return JsonResponse(result)

# def manager(request):return render(request,'fontpage/manager.html')