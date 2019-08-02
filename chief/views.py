from django.shortcuts import render, redirect
from Journal.pylink import *
from django.contrib import messages
from django.contrib.auth import logout
import os
from django.conf import settings
from django.http import FileResponse
from django.utils.http import urlquote

def main(request):
    """check if the user has login"""
    if not request.session.get('is_login', None):
        messages.success(request, '请登录后再进入！')
        return redirect("homepage:index")
    else:
        connection = pymysql.connect(host='127.0.0.1',
                                     user='root',
                                     passwd='19971111',
                                     db='periodic')

        sql = "SELECT periodic.article.articleid, periodic.article.title  from periodic.article WHERE  periodic.article.status= '水平编委审阅' "
        df = pd.read_sql(sql, connection)
        connection.close()

        data = []
        for i in range(0, len(df)):
            data.append(df.iloc[i])
        data = tuple(data)
        return render(request,'主编审查主界面.html',{'a_data':data})

def censor(request):
    if not request.session.get('is_login', None):
        messages.success(request, '请登录后再进入！')
        return redirect("homepage:index")
    else:

        return render(request, '主编审阅界面.html', )



def manage(request):
    if not request.session.get('is_login', None):
        messages.success(request, '请登录后再进入！')
        return redirect("homepage:index")
    else:
        connection = pymysql.connect(host='127.0.0.1',
                                     user='root',
                                     passwd='19971111',
                                     db='periodic')

        sql = "SELECT authorid, name, identity, tel, email " \
              "from periodic.author"

        df = pd.read_sql(sql, connection)
        connection.close()

        pos_dic = {'author': '作者', 'chief': '主编', 'editor': '编辑', 'member': '编委', 'expert': '专家'}
        df = df.replace(pos_dic)
        df = df.rename(columns = {'name':'aname','identity':'ident'})
        data = []
        for i in range(0,len(df)):
            data.append(df.iloc[i])
        data = tuple(data)

        return render(request, '主编人事管理主界面.html', {'author_data':data})


def add(request):
    if not request.session.get('is_login', None) :
        messages.success(request, '请登录后再进入！')
        return redirect("homepage:index")

    if request.session.get('identity', None) != 'chief':
        messages.success(request, '您不是主编，没有权限！')
        return redirect("homepage:index")

    if request.method == 'POST':
        userid = request.POST.get('userid', None)
        username = request.POST.get('username', None)
        pwd = request.POST.get('pwd', None)
        pos = request.POST.get('pos', None)
        tel = request.POST.get('tel', None)
        email = request.POST.get('email', None)
        islevel = request.POST.get('islevel', None)
        if islevel !='':
            islevel = int(islevel)
        isfield = request.POST.get('isfield', None)
        if isfield !='':
            isfield = int(isfield)
        field = request.POST.get('field', None)

        msg = None
        def add_faculty(request,uid, uname, tel, email, password, position, islevel, isfield, field):
            sql = "select * from periodic.author where authorid = '%s'" % uid
            if cnt(sql):
                messages.success(request, '人员ID已存在')
                return False
            sql1 = "insert into periodic.author values ('%s','%s','%s', '%s', '%s')" % (
            uid, uname, tel, position, email)
            sql2 = "insert into periodic.login values ('%s','%s', '%s')" % (uid, password, position)

            exe(sql1)
            exe(sql2)
            if (position != 'author'):
                sql3 = "insert into periodic.reviewer values ('%s','%s','%s', '%s', '%s')" % (
                uid, uname, tel, position, email)
                exe(sql3)
            try:
                if (position == 'expert'):
                    sql4 = "insert into periodic.expert values ('%s', '%s') " % (uid, field)
                    exe(sql4)
                if (position == 'member'):
                    if (isfield == 1):
                        sql5 = "insert into periodic.member values ('%s', '%s', '%s', '%s')" % (
                        uid, islevel, isfield, field)
                    else:
                        sql5 = "insert into periodic.member values ('%s', %d, %d)" % (uid, islevel, isfield)
                    exe(sql5)

            except:
                msg = False  # "人员信息添加出错"
            else:
                msg = True  # "人员信息添加成功"
            return msg

        msg = add_faculty(request,userid, username, tel, email, pwd, pos, islevel, isfield, field)

        if msg:
            messages.success(request, '人员信息添加成功！')

        else:
            messages.success(request, '人员信息添加失败。')

    return render(request, '主编人事信息添加界面.html')


def user_logout(request):
    logout(request)
    return redirect("homepage:index")


def chief_accept(request):
    artid = request.GET.get('artid')
    accept(artid)
    return redirect('chief:main')

def chief_reject(request):
    artid = request.GET.get('artid')
    reject(artid)
    return redirect('chief:main')



def delete_faculty(request):
    sql1 ="DELETE FROM periodic.author WHERE authorid = '%s'"% request.session['query_uid']

    sql2 = "DELETE FROM periodic.login WHERE id = '%s'" % request.session['query_uid']
    try:
        exe(sql1)
        exe(sql2)
    except:
        messages.success(request, '人员信息删除出错！')
        return redirect("chief:modify")
    else:
        messages.success(request, '人员信息删除成功！')
        return redirect("chief:manage")

def modify(request):
    if not request.session.get('is_login', None) :
        messages.success(request, '请登录后再进入！')
        return redirect("homepage:index")

    if request.session.get('identity', None) != 'chief':
        messages.success(request, '您不是主编，没有权限！')
        return redirect("homepage:index")

    userid = request.GET.get("userid")
    if userid is not None:
        request.session['query_uid'] = userid

    sql1 = "select * from author where authorid = '%s'"%request.session.get('query_uid')
    result = resy(sql1)

    sql2 = "select password from periodic.login where id = '%s'"%request.session.get('query_uid')
    pwd = resy(sql2)[0][0]

    is_field = None
    is_level = None
    field_1 = None
    if result[0][3] == 'expert':
        sql = "select field from periodic.expert where expertid = '%s'"%request.session.get('query_uid')
        field_1 = resy(sql)[0][0]
    if result[0][3] == 'member':
        sql = "select * from periodic.member where memberid = '%s'"%request.session.get('query_uid')
        res_1 = resy(sql)
        is_field = res_1[0][1]
        is_level = res_1[0][2]
        field_1 = res_1[0][3]

    if request.method == 'POST':
        userid = request.POST.get('userid', None)
        uname = request.POST.get('username', None)
        pwd = request.POST.get('pwd', None)
        pos = request.POST.get('pos', None)
        tel = request.POST.get('tel', None)
        email = request.POST.get('email', None)
        field = request.POST.get('field', None)
        isfield = request.POST.get('isfield', None)
        if isfield !='':
            isfield = int(isfield)
        islevel = request.POST.get('islevel', None)
        if islevel !='':
            islevel = int(islevel)

        sql1 ="UPDATE periodic.author SET periodic.author.name = '%s', " \
          "tel = '%s', periodic.author.identity ='%s', email = '%s' " \
          "WHERE authorid = '%s'"  % (uname, tel, pos, email, userid)

        sql2 = "UPDATE periodic.login SET password = '%s' " \
           "WHERE id = '%s'" % (pwd, userid)

        exe(sql1)
        exe(sql2)


        if(pos != 'author'):
            sql3 = "UPDATE periodic.reviewer SET periodic.reviewertel ='%s', " \
                   "periodic.reviewer.identity = '%s', email = '%s' where " \
                   "reviewerid = '%s'" % (tel, pos, email, userid)
            exe(sql3)

        try:
            if(pos == 'expert'):
                sql4 = "UPDATE periodic.expert SET field = '%s' " \
                "WHERE id = '%s'" % (field, userid)
            if (pos == 'member'):
                if (isfield == 1):
                    sql4 = "UPDATE periodic.member SET islevel = '%s', " \
                           "isfield = '%s', field = '%s' WHERE memberid = '%s'" % (islevel, isfield, field, userid)
                else:
                    sql4 = "UPDATE periodic.member SET islevel = '%s', " \
                           "isfield = '%s' WHERE memberid = '%s'" % (islevel, isfield, userid)
            exe(sql4)
        except:
            messages.success(request, '人员信息更改出错！')
        else:
            messages.success(request, '人员信息更改成功！')
    return render(request, '主编人事信息更改界面.html',
              {"userid": request.session['query_uid'], "username": result[0][1], "tel": result[0][2],
               "identity": result[0][3], "email": result[0][4], "pwd": pwd, "isfield":is_field, "islevel":is_level, "field":field_1})


def censor_detail(request):
    if not request.session.get('is_login', None) :
        messages.success(request, '请登录后再进入！')
        return redirect("homepage:index")

    if request.session.get('identity', None) != 'chief':
        messages.success(request, '您不是主编，没有权限！')
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

        msg = add_advise_chief(articleid, rid, ad)


        if msg:
            messages.success(request, '意见添加成功！')
            return redirect("chief:main")

        else:
            messages.success(request, '意见添加失败。')

    return render(request, '主编审阅界面.html',{"aid":request.session.get("query_aid"),"title":request.session.get("query_tt")})

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

def chief_modify(request):
    aid = request.session.get("query_aid")

    if modify_chief(aid):
        messages.success(request, '修改成功！')
        return redirect('chief:main')
    else:
        messages.success(request, '修改失败！')
        return redirect('chief:censor_detail')