# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from mysite.tools.Class_ElasticSearch import ElasticSearch
import time
import hashlib
from django.http import JsonResponse
from django.http import HttpResponseRedirect
# Create your views here.

# test
# def test(request):
#     from subprocess import Popen, PIPE
#     path = "/root/project/SearchApp/mysite/mysite/tools/Class_port_scan.py"
#     cmd = ['sudo', '-S', 'python3', path,"10.100.47.246"]
#     passwd = '123qwe'
#     p = Popen(cmd, stdin=PIPE, stderr=PIPE, universal_newlines=True, stdout=PIPE)
#     output = p.communicate(passwd + '\n')
#     return JsonResponse({"asd":output})


def index(request):
    """
    渲染html文件,获取主页
    """
    res = ElasticSearch().getData_number()
    data_num = res["hits"]["total"]
    user_name = None
    request.session.set_expiry(0)
    if request.session.get("isLogin"):
        user_name = request.session.get("isLogin")
        # 判断用户是否被禁用(处理用户已登录的时候禁用的操作)
        from searchapp.models import search_user
        if search_user.objects.get(name=user_name).flag == 1:
            del request.session["isLogin"]
            return HttpResponseRedirect("/")
    return render(request, "searchapp/index.html",
                  {"data_num": data_num, "user_name": user_name})


def dataanal(request):
    """
    渲染数据分析页面
    """
    res = ElasticSearch().getData_number()
    data_num = res["hits"]["total"]
    user_name = None
    if request.session.get("isLogin"):
        user_name = request.session.get("isLogin")
        # 判断用户是否被禁用(处理用户已登录的时候禁用的操作)
        from searchapp.models import search_user
        if search_user.objects.get(name=user_name).flag == 1:
            del request.session["isLogin"]
            return HttpResponseRedirect("/")
    return render(request, "searchapp/seh_dataAnal.html",
                  {"data_num": data_num, "user_name": user_name})


def getwebdata(request):
    """
    获取数据信息在前端形成图表
    """
    webdata = ElasticSearch().get_webapps_num()
    product = ElasticSearch().get_zujian_num()
    return JsonResponse({"webdata": webdata, "product": product})


def help(request):
    """
    渲染帮助页面
    """
    user_name = None
    if request.session.get("isLogin"):
        user_name = request.session.get("isLogin")
        # 判断用户是否被禁用(处理用户已登录的时候禁用的操作)
        from searchapp.models import search_user
        if search_user.objects.get(name=user_name).flag == 1:
            del request.session["isLogin"]
            return HttpResponseRedirect("/")
    return render(request, "searchapp/seh_help.html",
                  {"user_name": user_name})


def about(request):
    """
    渲染关于页面
    """
    user_name = None
    if request.session.get("isLogin"):
        user_name = request.session.get("isLogin")
        # 判断用户是否被禁用(处理用户已登录的时候禁用的操作)
        from searchapp.models import search_user
        if search_user.objects.get(name=user_name).flag == 1:
            del request.session["isLogin"]
            return HttpResponseRedirect("/")
    return render(request, "searchapp/seh_about.html",
                  {"user_name": user_name})


def contact(request):
    """
    渲染关于我们页面
    """
    user_name = None
    if request.session.get("isLogin"):
        user_name = request.session.get("isLogin")
        # 判断用户是否被禁用(处理用户已登录的时候禁用的操作)
        from searchapp.models import search_user
        if search_user.objects.get(name=user_name).flag == 1:
            del request.session["isLogin"]
            return HttpResponseRedirect("/")
    return render(request, "searchapp/seh_contact.html",
                  {"user_name": user_name})


def get_contact(request):
    """
    处理提交的反馈信息
    :param request:text 、code、type
    :type request:
    :return: state
    :rtype: json
    """
    # 判断用户是否存在
    user_name = None
    if request.session.get("isLogin"):
        user_name = request.session.get("isLogin")
    else:
        return HttpResponseRedirect("/")
    # 判断用户是否被禁用(处理用户已登录的时候禁用的操作)
    from searchapp.models import search_user
    if search_user.objects.get(name=user_name).flag == 1:
        del request.session["isLogin"]
        return HttpResponseRedirect("/")

    """
    获取建议
    还没有进行XSS检测
    """
    if not request.session.get("isLogin"):
        return HttpResponse(404)
    text = request.POST.get("text")
    choice = request.POST.get("choice")
    sendcode = request.POST.get('code')
    # xss 数据过滤 不应该直接将数据存入

    # 存入数据库
    getcode = request.session.get("code").lower()
    if sendcode != getcode:
        return JsonResponse({"info": 1})
    choice = int(choice)
    choice_list = ["合作需求", "账号权限", "隐私保护", "加入我们", "意见反馈"]
    from searchapp.models import articlev2
    user_name = request.session.get("isLogin")
    articlev2.objects.create(
        name=user_name,
        title=choice_list[choice],
        text=text,
        flag=0)
    return JsonResponse({"info": 0})


def getdata(request):
    """
    获取搜索的数据 一次去10条
    :param request:
    :type request:
    :return:
    :rtype:
    """
    # 判断用户是否存在
    user_name = None
    if request.session.get("isLogin"):
        user_name = request.session.get("isLogin")
    else:
        return HttpResponseRedirect("/")
    # 判断用户是否被禁用(处理用户已登录的时候禁用的操作)
    from searchapp.models import search_user
    if search_user.objects.get(name=user_name).flag == 1:
        del request.session["isLogin"]
        return HttpResponseRedirect("/")
    """
    获取主页请求数据并返回
    """
    msg = request.GET.get("search_msg")
    msg.strip()
    page = request.GET.get("page")
    try:
        page = int(page)
    except BaseException:
        page = 1
    # 分析语法、错误处理、语法是否合法尚未判断 均在底层实现 这里只做简单的处理,去掉最后一个;
    msgs = msg.split(";")
    if msgs[-1] == "":
        msgs.pop()
    start_time = time.time()
    res = ElasticSearch().search(msgs, page=page)
    end_time = time.time()
    search_time = float("%.2f" % (end_time - start_time))
    tag = msg
    try:
        total = res["hits"]["total"]
        hits_list = []
        for hit in res["hits"]["hits"]:
            hits_dict = {}
            hits_dict["ip"] = hit["_source"]["ip"]
            hits_dict["read"] = hit["_source"]["read"]
            hits_dict["server"] = hit["_source"]["server"]
            hits_dict["prowerd"] = hit["_source"]["prower"]
            hits_dict["title"] = hit["_source"]["title"]
            hits_dict["timestamp"] = hit["_source"]["timestamp"]
            hits_list.append(hits_dict)
        return render(request,
                      "searchapp/seh_showData.html",
                      {"page": page,
                       "total": total,
                       "time": search_time,
                       "tag": tag,
                       "all_hits": hits_list, "user_name": user_name})
    except BaseException:
        return render(request,
                      "searchapp/seh_showData.html",
                      {"page": 0,
                       "total": 0,
                       "time": search_time,
                       "tag": tag,
                       "all_hits": None, "user_name": user_name})


def detial(request):
    """
    获取详情页面
    :param request:
    :type request:
    :return:
    :rtype:
    """
    user_name = None
    if request.session.get("isLogin"):
        user_name = request.session.get("isLogin")
    else:
        return HttpResponseRedirect("/")
    # 判断用户是否被禁用(处理用户已登录的时候禁用的操作)
    from searchapp.models import search_user
    if search_user.objects.get(name=user_name).flag == 1:
        del request.session["isLogin"]
        return HttpResponseRedirect("/")
    from mysite.tools.Class_IPinfo import ipinfo
    ip = request.GET.get("ip")
    server = request.GET.get("server")
    prowerd = request.GET.get("prowerd")
    title = request.GET.get("title")

    data = ipinfo(ip).get_ipinfo()

    # ======老办法,速度慢=======
    # dom = DomainInfo(ip)
    # data = dom.getIpInfo()
    data["LN"] = data["location"]["latitude"]
    data["LE"] = data["location"]["longitude"]
    user_name = None
    if request.session.get("isLogin"):
        user_name = request.session.get("isLogin")
    data["user_name"] = user_name
    data["server"] = server
    data["prowerd"] = prowerd
    data["title"] = title
    data["read"] = ElasticSearch().getRead(ip)
    data["ip"] = ip
    return render(request, "searchapp/seh_detial.html", data)


def get_scanport(request):
    """
    扫描一个ip的开放端口
    :param request:
    :type request:
    :return:
    :rtype:
    """
    ip = request.GET.get("ip")
    from searchapp.models import ports_data
    try:
        msg = ports_data.objects.get(ip=ip)
        ports = msg.ports
        port = {}
        port["os"] = msg.os
        port["hostname"] = msg.hostname
        port["ports"] = eval(ports)
    except BaseException:
        # return JsonResponse({"error": 1}, status=500)
        from mysite.tools.Class_port_scan import port_scan
        try:
            port = port_scan(dst_ip=ip).scan_port()
        except Exception as e:
            return JsonResponse({"error": e}, status=500)
        portstr = str(port["ports"])
        if port["ports"] != []:
            ports_data.objects.create(
                ip=ip,
                os=port["os"],
                hostname=port["hostname"],
                ports=portstr)
    return JsonResponse(port)


def ajax_process(request):
    """
    处理登录数据
    """
    from .models import search_user
    data = {"login_info": None}
    email = request.POST.get("email").strip()
    paswd = request.POST.get("paswd")
    sendcode = request.POST.get("code").lower()
    getcode = request.session.get("code").lower()
    if sendcode != getcode:
        data["login_info"] = 2
        responce = JsonResponse(data)
        responce.status_code = 200
        return responce
    if request.is_ajax() and email and paswd:
        try:
            """
            OK
            """
            user = search_user.objects.get(
                email=email, password=encryption(paswd))
            if user.flag == 1:
                data["login_info"] = 3
            elif user.flag == 0:
                data["login_info"] = 0
                request.session["isLogin"] = user.name

        except Exception as e:
            """
            帐号或密码错误
            """
            data["login_info"] = 1
        responce = JsonResponse(data)
        responce.status_code = 200
        return responce
    else:
        """
        处理不是ajax的错误提交
        """
        data["login_info"] = "Bad Request"
        responce = JsonResponse(data)
        responce.status_code = 400
        return responce


def logout_process(request):
    """
    处理登出
    :param request:
    :type request:
    :return:
    :rtype:
    """
    sender_name = request.GET.get("user")
    try:
        get_name = request.session["isLogin"]
    except Exception as e:

        return JsonResponse(data={"logout_info": 2}, status=200)
    if sender_name != get_name:
        """
        防止恶意请求
        """
        return JsonResponse(data={"logout_info": 1}, status=400)
    try:
        del request.session["isLogin"]
    except Exception as e:
        """
        注销用户不存在, 处理跳转到400页面 Bad Request
        """
        return JsonResponse(data={"logout_info": 2}, status=200)
    return JsonResponse(data={"logout_info": 2}, status=200)


def create_code(request):
    """
    生成验证码
    """
    from io import BytesIO
    from mysite.tools.Class_getCode import getcode
    f = BytesIO()
    img, code = getcode().create()
    img.save(f, "PNG")
    request.session["code"] = code
    return HttpResponse(f.getvalue())


def sendEmail(request):
    """
    发送邮件(邮件格式验证还没有加)
    """
    from django.core.mail import send_mail
    import random
    email = request.POST.get("email")
    if check_email(email):
        return HttpResponse(status=400)
    codes = []
    for i in range(4):
        code = chr(random.randint(65, 90))
        codes.append(code)
    codes = "".join(codes)
    str = """
    Hello, this is the mailbox verification code (10 minutes valid)
    """ + codes + """
    From the elloit team.Have a good day :)
    """
    try:
        res = send_mail(
            '邮箱验证(SearchApp)',
            str,
            '18238670823@163.com',
            [email],
            fail_silently=False)
    except BaseException:
        pass

    if res == 1:
        request.session["email_code"] = codes
    return HttpResponse(res)


def register_process(request):
    """
    注册处理
    """
    email = request.POST.get("email").strip()
    name = request.POST.get("name").strip()
    paswd = request.POST.get("paswd").strip()
    email_code = request.POST.get("email_code").strip()
    data = {"reg_info": None}
    if(email_code != request.session.get("email_code")):
        # 验证码错误
        data["reg_info"] = 0
    elif check_email(email):
        # 邮箱已经注册
        data["reg_info"] = 1
    elif check_name(name):
        # 用户名一存在
        data["reg_info"] = 2
    elif len(paswd) < 6:
        # 密码太短
        data["reg_info"] = 3
    else:
        data["reg_info"] = 4
        from searchapp.models import search_user
        search_user.objects.create(
            name=name,
            password=encryption(paswd),
            email=email, flag=0)
        # 0 表示可以登陆 1 表示禁止状态
        del request.session["email_code"]
        request.session["isLogin"] = name
    return JsonResponse(data)


def check_name(name):
    """
    检查用户是否存在
    :param name:
    :type name:
    :return:
    :rtype:
    """
    from .models import search_user
    try:
        search_user.objects.get(name=name)
        return True
    except BaseException:
        return False


def check_email(email):
    """
    检测邮箱是是否已注册
    :param email:
    :type email:
    :return:
    :rtype:
    """
    from .models import search_user
    try:
        search_user.objects.get(email=email)
        return True
    except BaseException:
        return False


def encryption(str):
    """
    md5 加密 存储用户密码
    经过两次md5加密 取中间16位
    """
    m = hashlib.md5()
    m.update(str.encode("UTF-8"))
    text = m.hexdigest()
    m.update(text.encode("UTF-8"))
    return m.hexdigest()[8:-8]


def forgetpaswd(request):
    """
    处理忘记密码
    :param request:
    :type request:
    :return:
    :rtype:
    """
    email = request.POST.get("email")
    from .models import search_user
    try:
        get_email = search_user.objects.get(email=email).email
    except Exception as e:
        # 邮箱不存在
        return JsonResponse(data={"isExit": 0})
    # 邮箱存在 发送校验码
    from django.core.mail import send_mail
    import random
    codes = []
    for i in range(10):
        code = chr(random.randint(65, 90))
        codes.append(code)
    codes = "".join(codes)
    codes = encryption(codes)
    str = """
        Hello, 你的校验码为:
        """ + codes + """
        From the elloit team.Have a good day :)
        """
    try:
        res = send_mail(
            '找回密码(SearchApp)',
            str,
            '18238670823@163.com',
            [get_email],
            fail_silently=False)
    except BaseException:
        pass
    if res == 1:
        request.session["forget_code"] = codes
        request.session["chang_email"] = get_email
    return JsonResponse(data={"isExit": 1})


def changepaswd(request):
    """
    修改密码
    :param request:
    :type request:
    :return:
    :rtype:
    """
    code = request.POST.get("code").strip()
    newpasswd = request.POST.get("newpasswd").strip()
    if not code and not newpasswd:
        return HttpResponse(status=400)
    else:
        try:
            getcode = request.session.get("forget_code")
            chang_email = request.session.get("chang_email")
        except BaseException:
            return HttpResponse(status=400)
        if code != getcode:  # 校验码错误
            return JsonResponse({"changinfo": 0})
        else:
            from .models import search_user
            obj = search_user.objects.get(email=chang_email)
            obj.password = encryption(newpasswd)
            obj.save()
            del request.session["forget_code"]
            del request.session["chang_email"]
            return JsonResponse({"changinfo": 1})


#===========================================忽略以下代码========================
# def jump(request, a, b):
#     """
#     跳转
#     :param request:
#     :type request:
#     :return:
#     :rtype:
#     """
#     return HttpResponseRedirect(
#         reverse("add2", args=(a, b))
#     )
#
#
# def hello(request):
#     str = "Hello 我是从后台传来的变量"
#
#     data = {
#         "info": {
#             "hello": str,
#             "name": "Elloit",
#             "age": 10,
#             "addr": "中国宇宙"
#         }
#     }
#
#     return render(request, "searchapp/responce.html", data)
#
#
# def get_sum(request):
#     return render(request, "searchapp/Froms.html")
#
#
# def sum_post(request):
#
#     a = request.POST.get("a", 0)
#     b = request.POST.get("b", 0)
#     res = int(a) + int(b)
#     return render(request, "searchapp/Froms.html",
#                   {"res_post": res, "a_post": a, "b_post": b})
#
#
# def sum(request):
#     # a = request.GET["a"]
#     # b = request.GET["b"]
#     a = request.GET.get("a", 0)
#     b = request.GET.get("b", 0)
#     res = int(a) + int(b)
#     # return HttpResponse(str(res))
#     return render(request, "searchapp/Froms.html",
#                   {"res": res, "a": a, "b": b})
#
#
# def sum2(request, a, b):
#
#     res = int(a) + int(b)
#     return HttpResponse(str(res))
