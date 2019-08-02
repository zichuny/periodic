from django.shortcuts import render, redirect, reverse
from Journal.pylink import *
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import os
from django.contrib.auth import logout

# Create your views here.


def author_contribute(request):
    if not request.session.get('is_login', None):
        return redirect("homepage:index")
    id = request.session['id']
    artli = paper(id)
    return render(request, '用户已投稿件界面.html', {'artli':artli})


def contribute(request):
    if not request.session.get('is_login', None):
        return redirect("homepage:index")
    return render(request, '用户在线投稿界面.html')


def modify(request):
    if not request.session.get('is_login', None):
        return redirect("homepage:index")
    #显示修改意见
    autid = request.GET.get('authorid')
    rid = request.session['id']
    if autid != rid:
        return HttpResponseRedirect(reverse('homepage:index'))
    artid = request.GET.get('artid')
    data = feedback(artid)
    return render(request, '用户稿件修改界面.html', {'data1':data})

# 上传新文件
def reupload(request):
    if request.method == "POST":
        ititle = request.POST.get('ititle', None)
        ifield = request.POST.get('ifield', None)
        f = request.FILES["file"]
        body = f.name
        artid = request.GET.get('artid')
        result = reuploadfile(ititle, ifield, body, artid)
        if result > 0:
            filePath = os.path.join(settings.MDEIA_ROOT, f.name)
            extension = os.path.splitext(filePath)[1]
            with open(filePath, 'wb') as fp:
                for info in f.chunks():
                    fp.write(info)
            filename = str(result) + extension
            new_file = os.path.join(settings.MDEIA_ROOT, filename)
            os.remove(new_file)
            os.rename(filePath, new_file)
            change_status(artid)
            return render(request, '用户稿件修改成功界面.html')
        else:
            return HttpResponse("上传失败！")
    else:
        return HttpResponse("上传失败！")


def savefile(request):
    if not request.session.get('is_login', None):
        return redirect("homepage:index")
    if request.method == "POST":
        id = request.session['id']
        ititle = request.POST.get('ititle', None)
        ifield = request.POST.get('ifield', None)
        f = request.FILES["file"]
        body = f.name
        result = upload(id, ititle, ifield, body)
        if result > 0:
            filePath = os.path.join(settings.MDEIA_ROOT, f.name)
            extension = os.path.splitext(filePath)[1]
            with open(filePath, 'wb') as fp:
                for info in f.chunks():
                    fp.write(info)
            filename = str(result) + extension
            new_file = os.path.join(settings.MDEIA_ROOT, filename)
            os.rename(filePath, new_file)
            return render(request, '用户在线投稿成功界面.html')
        else:
            return HttpResponse("上传失败！")
    else:
        return HttpResponse("上传失败！")


# 查询按钮
def data_fresh(request):
    if not request.session.get('is_login', None):
        return HttpResponseRedirect(reverse('homepage:index'))
    ititle = request.GET.get('ititle', None)
    ishenyue = request.GET.get("ishenyue", None)
    ibegintime = request.GET.get("ibegintime", None)
    if ibegintime == 'NaN':
        start = datetime.date(2000, 1, 1)
    else:
        start = datetime.datetime.fromtimestamp(int(ibegintime) / 1000)
    iendtime = request.GET.get("iendtime", None)
    if iendtime == 'NaN':
        end = datetime.date(2030, 1, 1)
    else:
        end = datetime.datetime.fromtimestamp(int(iendtime) / 1000)
    iid = request.session['id']
    li = []
    if ishenyue == "如需查询状态请选择一状态":
        #查询所有符合状态的文章
        ar = search(iid,start,end,ititle)
    else:
        ar = search_shenyue(iid,start,end,ititle,ishenyue)
    for a in ar:
        li.append(
            [a[0], a[1], a[2], a[3], a[4], a[5]])
    return JsonResponse({"da": li})

def user_logout(request):
    logout(request)
    return redirect("/homepage/index")