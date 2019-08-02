from django.shortcuts import render, redirect
from Journal.pylink import *
from django.contrib import messages
from django.contrib.auth import logout
import os
from django.conf import settings
from django.http import FileResponse
from django.utils.http import urlquote

# Create your views here.
def main_field(request):
    """check if the user has login"""

    if not request.session.get('is_login', None):
        messages.success(request, '请登录后再进入！')
        return redirect("homepage:index")
    if request.session['isfield'] != [1]:
        print(type(request.session['isfield']))
        messages.success(request, '您不是责任编辑，没有权限！')
        return redirect("member:main_level")
    else:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     passwd='19971111',
                                     db='periodic')
        sql = "SELECT articleid, title from periodic.article WHERE  status= '编辑审阅' "
        df = pd.read_sql(sql, connection)
        connection.close()

        data = []
        for i in range(0, len(df)):
            data.append(df.iloc[i])
        data = tuple(data)
        return render(request,'编委领域审查主界面.html',{'a_data':data})

def main_level(request):
    """check if the user has login"""
    if not request.session.get('is_login', None):
        messages.success(request, '请登录后再进入！')
        return redirect("homepage:index")
    if request.session['islevel'] != [1]:
        print(request.session['islevel'])
        messages.success(request, '您不是水平编委，没有权限！')
        return redirect("member:main")
    else:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     passwd='19971111',
                                     db='periodic')
        sql = "SELECT articleid, title from periodic.article WHERE  status= '责任编委审阅' "
        df = pd.read_sql(sql, connection)
        connection.close()

        data = []
        for i in range(0, len(df)):
            data.append(df.iloc[i])
        data = tuple(data)
        return render(request,'编委水平审查主界面.html',{'a_data':data})

def user_logout(request):
    logout(request)
    return redirect("homepage/index")

def censor(request):
    if not request.session.get('is_login', None) :
        messages.success(request, '请登录后再进入！')
        return redirect("homepage:index")

    if request.session.get('identity', None) != 'member':
        messages.success(request, '您不是编辑，没有权限！')
        return redirect("homepage:index")

    articleid = request.GET.get("articleid")
    title = request.GET.get("title")
    if articleid is not None:
        request.session['query_aid'] = articleid
        request.session['query_tt'] = title


    if request.method == 'POST':
        articleid = request.POST.get('aid', None)
        rid = request.session.get('id')
        ad = request.POST.get('textarea', None)

        msg = add_advise_field(articleid, rid, ad)

        if msg:
            messages.success(request, '意见添加成功！')
            return redirect("member:main")

        else:
            messages.success(request, '意见添加失败。')

    return render(request, '编委领域审阅界面.html',{"aid":request.session.get("query_aid"),"title":request.session.get("query_tt")})

def censor_level(request):
    if not request.session.get('is_login', None) :
        messages.success(request, '请登录后再进入！')
        return redirect("homepage:index")

    if request.session.get('identity', None) != 'member':
        messages.success(request, '您不是编辑，没有权限！')
        return redirect("homepage:index")

    articleid = request.GET.get("articleid")
    title = request.GET.get("title")
    if articleid is not None:
        request.session['query_aid'] = articleid
        request.session['query_tt'] = title


    if request.method == 'POST':
        articleid = request.POST.get('aid', None)
        rid = request.session.get('id')
        ad = request.POST.get('textarea', None)

        msg = add_advise_level(articleid, rid, ad)
        if msg:
            messages.success(request, '意见添加成功！')
            return redirect("member:main")
        else:
            messages.success(request, '意见添加失败。')

    return render(request, '编委水平审阅界面.html',{"aid":request.session.get("query_aid"),"title":request.session.get("query_tt")})

def return_main(request):
    return redirect("/member/main")

def member_accept(request):
    aid = request.session.get("query_aid")

    if pass_field(aid):
        messages.success(request, '通过成功！')
        return redirect('member:main')
    else:
        messages.success(request, '操作失败！')
        return redirect('member:censor')

def member_modify(request):
    aid = request.session.get("query_aid")

    if modify_field(aid):
        messages.success(request, '拒绝成功！')
        return redirect('member:main')
    else:
        messages.success(request, '系统出错，请重试！')
        return redirect('member:censor')


def member_accept_level(request):
    aid = request.session.get("query_aid")

    if pass_level(aid):
        messages.success(request, '通过成功！')
        return redirect('member:main')
    else:
        messages.success(request, '操作失败！')
        return redirect('member:censor')

def member_modify_level(request):
    aid = request.session.get("query_aid")

    if modify_level(aid):
        messages.success(request, '修改成功！')
        return redirect('member:main')
    else:
        messages.success(request, '修改失败！')
        return redirect('member:censor')


def download(request):
    artid=request.session.get("query_aid")#文件名称，包含后缀
    name = aname(artid)
    filePath = os.path.join(settings.MDEIA_ROOT, name)
    extension = os.path.splitext(filePath)[1]
    name2 = artid + extension
    filePath = os.path.join(settings.MDEIA_ROOT, name2)#文件路径
    file = open(filePath, 'rb')
    response = FileResponse(file)

    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s"'%(urlquote(name))#输出文件名称
    return response

def level_reject(request):
    artid = request.GET.get('artid')
    reject(artid)
    return redirect('member:main')