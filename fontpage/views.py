#coding:utf-8
from django.shortcuts import render
from .models import Article,Usertable,Usergroup,Roletable
from django.http import JsonResponse
import datetime
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers 
import json
# Create your views here.
def index(request):
	 content=Article.objects.filter(a_issee=True)
	 content= json.loads(serializers.serialize("json", content))
	 return render(request,'fontpage/index.html',{'content':content})

def adminIndex(request):
	message={}
	if request.session.get('u_account',False):
		log_type=Roletable.objects.get(usertable__u_account=request.session['u_account'])
		if log_type.r_type=='manager':
			pageList=getSubmitPage()
			personList=PersonList(log_type.r_type)
			groupList=getGroup()
			#print pageList
			return render(request,'fontpage/manager.html',{'account':request.session['u_account'],'message':message,'pageList':pageList,'personList':personList,'groupList':groupList})
		elif log_type.r_type=='headman':
			personList=PersonList(log_type.r_type)
			return render(request,'fontpage/headman.html',{'account':request.session['u_account'],'message':message,'personList':personList})
		else:
			return render(request,'fontpage/member.html',{'account':request.session['u_account'],'message':message})
	else:
		return render(request,'fontpage/login.html')
@csrf_exempt
def deleteArticle(request):
	result={}
	if request.is_ajax():
		a_title=request.POST.get('a_title')
		u_account=request.POST.get('u_account')
		try:
			det_article=Article.objects.get(a_title=a_title)
			mod_user=Usertable.objects.get(u_account=u_account)
			det_score=mod_user.u_score
			mod_user.u_score=det_score-10
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
		a_time=datetime.datetime.now().strftime("%Y-%m-%d")
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
		if request.method=='POST':
			u_account=request.POST.get('u_account')
			u_password=request.POST.get('u_password')
			try:
				checkUser=Usertable.objects.get(u_account=u_account,u_password=u_password)
				request.session['u_account']=u_account
				result={}
				result['ret_code']=0
				result['ret_msg']=''
				return adminIndex(request)
			except Exception as e:
				return render(request,'fontpage/login.html',{'error':e,'account':u_account,'password':u_password})
		if request.method=='GET':
			return render(request,'fontpage/login.html',{'error':"ooo"})

def logout(request):
		result={}
		if request.session.get('u_account',False):
			del request.session['u_account']
			result['ret_code']=0
			result['ret_msg']="logout"
			return index(request)
		else:
			return render(request,'fontpage/login.html')

@csrf_exempt
def approve(request):
	result={}
	if request.is_ajax():
		a_title=request.POST.get('a_title')
		try:
			approve_article=Article.objects.get(a_title=a_title)
			approve_article.a_issee=True
			approve_article.save()
			provider=Usertable.objects.filter(article__a_title=a_title)
			for single in provider:
				single.u_score=single.u_score+10
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
		rec_account=request.session['u_account']
		rec_role=Roletable.objects.get(usertable__u_account=rec_account)
		if rec_role.r_type=="headman":
			new_group=Usergroup.objects.get(usertable__u_account=rec_account).g_name
		else:
			new_group=request.POST.get('u_group')
		print new_account
		try:
			no_re=Usertable.objects.get(u_account=new_account)
			result['ret_code']=-1
			result['ret_msg']="user already exist"
			print 222
		except Exception as e:
			u_group=Usergroup.objects.get(g_name=new_group)
			u_role=Roletable.objects.get(r_type=new_role)
			Usertable(g=u_group,r=u_role,u_account=new_account,u_password=new_password,u_nickname=new_nickname,u_score=new_score).save()
			sumperson=u_group.sumperson
			u_group.sumperson=sumperson+1
			u_group.save()
			result['ret_code']=0
			result['ret_msg']=''
		finally:
			return JsonResponse(result)
	else:
		result['ret_code']=-2
		result['ret_msg']="illegal"
		return JsonResponse(result)
@csrf_exempt
def removeUser(request):
	result={}
	if request.is_ajax():
		u_account=request.POST.get('u_account')
		try:
			re_user=Usertable.objects.get(u_account=u_account)
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
@csrf_exempt
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
	 		return JsonResponse(result)
	else:
	 	result['ret_code']=-2
		result['ret_msg']="illegal"
		return JsonResponse(result)
@csrf_exempt
def removeGroup(request):
	result={}
	if request.method=='POST':
		group_title=request.POST.get('g_name')
		try:
			re_group=Usergroup.objects.get(g_name=group_title)
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

def getGroup():
	result={}
	group_result=Usergroup.objects.all()
	result['ret_code']=0
	result['content']=json.loads(serializers.serialize("json", group_result))
	result['ret_msg']=''
	return result

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
	except Exception as e:
		print e
	result['ret_code']=0
	JsonContent=serializers.serialize("json", content)
	result['content']=json.loads(JsonContent)
	result['ret_msg']=''
	try:
		for index,values in enumerate(result['content']):
			values["fields"]["u"]=personForPage(values["fields"]["u"])
	except Exception as e:
		print e
	return result
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
			#print any(content)
		except Exception as e:
			print e
	elif r_type=='headman':
		content=Usertable.objects.filter(r__r_type="member")
	result['ret_code']=0
	result['content']=json.loads(serializers.serialize("json", content))
	result['ret_msg']=''
	return result

def personForPage(uid):
	try:
		personInfo=Usertable.objects.get(pk=uid)
	except Exception as e:
		print e
	return personInfo.u_account