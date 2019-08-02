import pandas as pd
import pymysql
import datetime,time
from dateutil.relativedelta import relativedelta
import os
from django.conf import settings
import uuid
import hashlib


'''
常用接口
'''
def resy(sql):
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 passwd='19971111',
                                 db='periodic')
    cursor = connection.cursor();
    cursor.execute(sql)
    result = cursor.fetchall();
    connection.commit();
    return result;


def res(sql):
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 passwd='19971111',
                                 db='periodic')
    data = pd.read_sql(sql, connection)
    connection.close()
    data = data.to_dict(orient='list')
    return data


def res_tuple(sql):
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 passwd='19971111',
                                 db='periodic')
    cursor = connection.cursor();
    cursor.execute(sql)
    result = cursor.fetchall();
    connection.commit();
    return result;


def exe(sql):
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 passwd='19971111',
                                 db='periodic')
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()


def cnt(sql):
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 passwd='19971111',
                                 db='periodic')
    cursor = connection.cursor()
    result = cursor.execute(sql)
    connection.commit()
    connection.close()
    return result


'''
登录注册界面
'''


# 登录验证
def signin(id, pwd):
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 passwd='19971111',
                                 db='periodic')
    sql = "Select * from periodic.login Where Id ='%s'" % id
    hl = hashlib.md5()
    hl.update(pwd.encode(encoding='utf-8'))
    md5password = hl.hexdigest()
    data = pd.read_sql(sql, connection)
    connection.close()
    data = data.to_dict(orient='list')
    res = 'unvalid'
    if data['Password'][0] == str(md5password):
        res = data['Identity'][0]
    return res


# 注册新用户
def signup_user(id, pwd, name, email, tele):
    sql0 = "Select * from periodic.login Where Id = '%s'" % id
    isdup = cnt(sql0)
    hl = hashlib.md5()
    hl.update(pwd.encode(encoding='utf-8'))
    md5password = hl.hexdigest()
    if isdup == 0:
        sql1 = "Insert into periodic.Author(AuthorID,Name,Tel,Email,Identity) values('%s','%s','%s','%s','author')" % (
            id, name, tele, email)
        sql2 = "Insert into periodic.Login(ID,Password,Identity) values('%s','%s','author')" % (id, md5password)
        try:
            exe(sql1)
            exe(sql2)
        except:
            return 'error'
        else:
            return 'done'
    else:
        return 'duplicate'

'''
忘记密码界面
'''
#随机生成验证码
def get_random_str():
    uuid_val = uuid.uuid4()
    uuid_str = str(uuid_val).encode("utf-8")
    md5 = hashlib.md5()
    md5.update(uuid_str)
    return md5.hexdigest()



#获得邮箱
def get_email(id):
    sql = "Select periodic.author.Email from periodic.author where periodic.author.AuthorID='%s'"%id
    email = res(sql)
    email = email['Email']
    return email

#修改密码
def change(id,pwd):
    hl = hashlib.md5()
    hl.update(pwd.encode(encoding='utf-8'))
    md5password = hl.hexdigest()
    sql = "Update periodic.login Set periodic.login.password = '%s' where periodic.login.ID = '%s'"%(md5password,id)
    try:
        exe(sql)
    except:
        return False
    else:
        return True

'''
作者界面
'''


def paper(id):
    sql = "Select periodic.article.Title,periodic.article.status,periodic.upload.Time," \
          "periodic.upload.LastEditTime,periodic.article.AuthorID,periodic.article.ArticleID from periodic.upload,periodic.article " \
          "where periodic.article.AuthorID = '%s' and periodic.upload.ArticleID=periodic.article.ArticleID" % id
    data = res_tuple(sql)
    return data


def search(id, start, end, title):
    endTime_str = datetime.datetime.strftime(end + relativedelta(days=1), "%Y-%m-%d")
    startTime_str = datetime.datetime.strftime(start, '%Y-%M-%d')
    sql = "Select periodic.article.Title,periodic.article.status,periodic.upload.Time," \
          "periodic.upload.LastEditTime,periodic.article.ArticleID,periodic.article.AuthorID from periodic.upload,periodic.article " \
          "where periodic.article.AuthorID = '%s' and periodic.upload.ArticleID=periodic.article.ArticleID and periodic.article.Title='%s' " \
          "and date_format(periodic.upload.Time,'%%Y-%%m-%%d')>= '%s' and date_format(periodic.upload.Time,'%%Y-%%m-%%d')<='%s'" % (
              id, title, startTime_str, endTime_str)
    data = res_tuple(sql)
    return data


def search_shenyue(iid, start, end, title, shenyue):
    endTime_str = datetime.datetime.strftime(end, "%Y-%m-%d") + relativedelta(days=1)
    startTime_str = datetime.datetime.strftime(start, '%Y-%M-%d')
    sql = "Select periodic.article.Title,periodic.article.status,periodic.upload.Time," \
          "periodic.upload.LastEditTime,periodic.article.ArticleID,periodic.article.AuthorID from periodic.upload,periodic.article " \
          "where periodic.article.AuthorID = '%s' and periodic.upload.ArticleID=periodic.article.ArticleID and periodic.article.Title='%s' " \
          "and date_format(periodic.upload.Time,'%%Y-%%m-%%d')>= '%s' and date_format(periodic.upload.Time,'%%Y-%%m-%%d')<='%s' and periodic.article.status = '%s'" % (
              id, title, startTime_str, endTime_str, shenyue)
    data = res(sql)
    return data


def upload(id, title, field, body):
    sql0 = "Select periodic.upload.AuthorID from periodic.upload"
    num = cnt(sql0)
    sql1 = "Insert into periodic.upload(AuthorID,ArticleID,Time,LastEditTime) values('%s','%s',NOW(),NOW())" % (
        id, str(num + 1))
    sql2 = "Insert into periodic.article(ArticleID,Title,Body,Status,Field,NumOfEdits,AuthorID) " \
           "values('%s','%s','%s','%s','%s','%d','%s')" % (str(num + 1), title, body, '待审核', field, 0, id)
    try:
        exe(sql2)
        exe(sql1)
    except:
        return -1
    else:
        return num + 1


def reuploadfile(title, field, body, artid):
    print(artid)
    artid = artid[2:]
    artid = artid[:-2]
    sql0 = "Select periodic.article.NumOfEdits from periodic.article where periodic.article.ArticleID='%s'" % artid
    noe = res(sql0)['NumOfEdits'][0]+1

    sql1 = "Update periodic.upload SET periodic.upload.LastEditTime = NOW() where periodic.upload.ArticleID = '%s'" % artid
    sql2 = "Update periodic.article SET periodic.article.Title = '%s',periodic.article.Field = '%s'," \
           "periodic.article.Body='%s',periodic.article.NumOfEdits = '%s' where periodic.article.ArticleID = '%s'" % (
               title, field, body, noe, artid)
    try:
        exe(sql2)
        exe(sql1)
    except:
        return -1
    else:
        return int(artid)
def change_status(artid):
    artid = artid[2:]
    artid = artid[:-2]
    sql0 = "Select periodic.article.status from periodic.article where periodic.article.ArticleID='%s'" % artid
    data = res(sql0)
    status=data['status'][0]
    if status == '水平编委待修改':
        sql1 = "Update periodic.article SET periodic.article.status = '责任编委审阅' where periodic.article.ArticleID='%s'"%artid
    if status == '主编待修改':
        sql1 = "Update periodic.article SET periodic.article.status = '水平编委审阅' where periodic.article.ArticleID='%s'"%artid
    exe(sql1)


def feedback(aid):
    sql0 = "Select periodic.article.status from periodic.article where periodic.article.ArticleID='%s'" % str(aid)
    data = res(sql0)
    status = data['status'][0]

    sql1 = "Select periodic.review_format.ReviewerID,periodic.review_format.Feedback,periodic.review_format.ArticleID from periodic.review_format " \
           "where periodic.review_format.ArticleID='%s'" % str(aid)
    format = res(sql1)
    data1 = list(format.values())


    sql2 = "Select a.ReviewerID,a.Feedback,a.ArticleID from periodic.review_field a where a.ArticleID='%s'" % str(aid)
    field = res(sql2)
    data2 = list(field.values())

    sql3 = "Select a.ReviewerID,a.Feedback,a.ArticleID from periodic.review_level a where a.ArticleID='%s'"% str(aid)
    level = res(sql3)
    data3 = list(level.values())

    if status == "主编待修改":
        data = data2
    elif status == "水平编委待修改":
        data = data3
    else:
        data = data1
    print(data)
    return data


'''
主编界面
'''
def add_advise_chief(aid, rid, ad):
    sql1 = "insert into periodic.review_level values ('%s','%s','%s',now())" % (aid, rid, ad)
    msg = None
    try:
        exe(sql1)
    except:
        msg = False
    else:
        msg = True
    return msg

def accept(artid):
    sql1 = "Update periodic.article Set periodic.article.status = '通过' where periodic.article.ArticleID='%s'"%artid
    try:
        exe(sql1)
    except:
        return False
    else:
        return True

def reject(artid):
    sql1 = "Update periodic.article Set periodic.article.status = '拒绝' where periodic.article.ArticleID='%s'"%artid
    try:
        exe(sql1)
    except:
        return False
    else:
        return True


def aname(aid):
    sql = "Select periodic.article.body from periodic.article where periodic.article.ArticleID='%s'"%aid
    body = res(sql)
    name = body['body'][0]
    return name

def modify_chief(aid):
    sql1 = "Update periodic.article Set periodic.article.status = '主编待修改' where periodic.article.ArticleID='%s'"%aid
    try:
        exe(sql1)
    except:
        return False
    else:
        return True


'''
编辑界面
'''
def add_advise_format(aid, rid, ad):
    sql1 = "insert into periodic.review_format values ('%s','%s','%s',now())" % (aid, rid, ad)
    msg = None
    try:
        exe(sql1)
    except:
        msg = False
    else:
        msg = True
    return msg

def pass_format(aid):
    sql1 = "Update periodic.article Set periodic.article.status = '编辑审阅' where periodic.article.ArticleID='%s'"%aid
    try:
        exe(sql1)
    except:
        return False
    else:
        return True

def modify_format(aid):
    sql1 = "Update periodic.article Set periodic.article.status = '编辑待修改' where periodic.article.ArticleID='%s'"%aid
    try:
        exe(sql1)
    except:
        return False
    else:
        return True

'''
领域/水平编委
'''

def add_advise_field(aid, rid, ad):
    sql1 = "insert into periodic.review_field values ('%s','%s','%s',now())" % (aid, rid, ad)
    msg = None
    try:
        exe(sql1)
    except:
        msg = False
    else:
        msg = True
    return msg


def pass_field(aid):
    sql1 = "Update periodic.article Set periodic.article.status = '责任编委审阅' where periodic.article.ArticleID='%s'"%aid
    try:
        exe(sql1)
    except:
        return False
    else:
        return True

def modify_field(aid):
    sql1 = "Update periodic.article Set periodic.article.status = '拒绝' where periodic.article.ArticleID='%s'"%aid
    try:
        exe(sql1)
    except:
        return False
    else:
        return True

def add_advise_level(aid, rid, ad):
    sql1 = "insert into periodic.review_level values ('%s','%s','%s',now())" % (aid, rid, ad)
    print(ad)
    msg = None
    try:
        exe(sql1)
    except:
        msg = False
    else:
        msg = True
    return msg

def pass_level(aid):
    sql1 = "Update periodic.article Set periodic.article.status = '水平编委审阅' where periodic.article.ArticleID='%s'"%aid
    try:
        exe(sql1)
    except:
        return False
    else:
        return True

def modify_level(aid):
    sql1 = "Update periodic.article Set periodic.article.status = '水平编委待修改' where periodic.article.ArticleID='%s'"%aid
    try:
        exe(sql1)
    except:
        return False
    else:
        return True

def field(id):
    sql = "Select periodic.member.isField from periodic.member where periodic.member.MemberID='%s'"%id
    f = res(sql)
    f = f['isField']
    return f

def level(id):
    sql = "Select periodic.member.isLevel from periodic.member where periodic.member.MemberID='%s'" % id
    l = res(sql)
    l = l['isLevel']
    return l