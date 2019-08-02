from django.shortcuts import render, redirect, HttpResponse
from Journal.pylink import *
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import random


def changepwd(request):
    id = request.session['gid']

    if request.method == 'POST':
        pwd = request.POST.get('pwd1',None)
        if change(id,pwd):
            return redirect('/homepage/index')
        else:
            return HttpResponse("密码设置失败")

    return render(request,'重置密码界面.html')

'''
def index(request):
    if request.method == 'POST':
        userid = request.POST.get('userid', None)
        pwd = request.POST.get('pwd', None)
        identity = signin(userid, pwd)
        if identity != 'unvalid':
            request.session['is_login'] = True
            request.session['id'] = userid
            request.session['identity'] = identity
        if signin(userid, pwd)=='author':
            #return render(request, '用户已投稿件界面.html')
            return  redirect('/author/author_contribute')
        elif signin(userid, pwd)=='editor':
            return render(request, '编辑主界面.html')
        elif signin(userid, pwd)=='chief':
            return render(request, '主编审查主界面.html')
        else:
            return redirect('/homepage/error')

    return render(request, '用户登录界面.html')
'''
def index(request):
    if request.method == 'POST':
        userid = request.POST.get('userid', None)
        pwd = request.POST.get('pwd', None)
        identity = signin(userid, pwd)
        is_field = field(userid)
        is_level = level(userid)
        if identity != 'unvalid':
            request.session['is_login'] = True
            request.session['id'] = userid
            request.session['identity'] = identity
            request.session['isfield']=is_field
            request.session['islevel']=is_level
        if signin(userid, pwd)=='author':
            return  redirect('/author/author_contribute')
        elif signin(userid, pwd)=='editor':
            return redirect("/editor/main")
        elif signin(userid, pwd)=='member' and is_field == [1]:
            return redirect("member:main")
        elif signin(userid, pwd)=='member' and is_level == [1]:
            return redirect("member:main_level")
        elif signin(userid, pwd)=='chief':
            return redirect("/chief/main")
        else:
            return redirect('/homepage/error')

    return render(request, '用户登录界面.html')

def forget(request):
    if request.method == 'POST':
        code = request.POST.get('u999919_input', None)
        print("code:",code)
        vcode = request.session['vcode']
        print("vcode",vcode)
        if code == vcode:
            return redirect('/homepage/changepwd')
    return render(request, '获取验证码界面.html')

def send_email(request):
    id = request.GET.get("userid", None)
    title = "Email Verification"
    #生成6位随机验证码
    vcode = []
    for i in range(6):
        alpha = chr(random.randint(65, 90))  # random.randrange(65,91)
        alpha_lower = chr(random.randint(97, 122))  # random.randrange(65.91)
        num = str(random.randint(0, 9))
        ret = random.choice([alpha, num, alpha_lower])
        vcode.append(ret)
    vcode = ''.join(vcode)
    request.session['vcode'] = vcode
    print("vcode:",vcode)
    msg = "Your Journal Studio verification code is" + vcode
    email_from = settings.DEFAULT_FROM_EMAIL
    if id is not None:
        request.session['gid'] = id
        print("id:",id)
    if id !=None:
        receiver = get_email(id)
        # 发送邮件
        try:
            send_mail(title, msg, email_from, receiver)
        except:
            print('fail')
        else:
            print('succeed')
    return JsonResponse({"vcode":vcode})

def signup(request):
    if request.method == 'POST':
        userid = request.POST.get('userid', None)
        pwd = request.POST.get('pwd1', None)
        name = request.POST.get('name',None)
        email = request.POST.get('email',None)
        tele = request.POST.get('tele',None)
        if signup_user(userid, pwd,name,email,tele)=='done':
            return render(request, '用户注册界面成功注册提示.html')
        elif signup_user(userid, pwd,name,email,tele)=='duplicate':
            return render(request,'用户注册界面用户名重复提示.html')
        else:
            messages.success(request,'注册失败！')
            return redirect('/homepage/signup')
    return render(request, '用户注册界面.html')


def error(request):
    return render(request, '登录界面错误提示.html')

