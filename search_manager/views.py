from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import time
import sys
import os
from mysite.tools.Class_get_system import Get_System
from mysite.tools.Class_ElasticSearch import ElasticSearch
# Create your views here.


def admin(request):
    """
    渲染 admin首页
    如果没有登陆就跳转到登陆页面
    """
    if request.session.get("isLogin_manger"):
        disk_state = Get_System().get_disk()
        ip = Get_System().get_ip()
        return render(request, "search_manager/" +
                      "index.html", {"disk": disk_state, "ip": ip})
    return render(request, "search_manager/smg_login.html")


def login_manager(request):
    """
    登陆
    """
    request.session.set_expiry(0)  # 设置session失效的时间 关闭浏览器就失效
    from django.contrib.auth.models import User
    name = request.POST.get("name", None)
    password = request.POST.get("paswd", None)
    if name is None or password is None:
        return JsonResponse({"info": 2}, status=400)
    try:
        u = User.objects.get(username=name)
    except BaseException:
        return JsonResponse({"info": 1})
    if not u.check_password(password):
        return JsonResponse({"info": 1})
    request.session["isLogin_manger"] = name
    return JsonResponse({"info": 0})


def logout(request):
    """
    登出
    :param request:
    :type request:
    :return:
    :rtype:
    """
    if request.session.get("isLogin_manger"):
        del request.session["isLogin_manger"]
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)


def index(request):
    """
    渲染首页
    """
    if not request.session.get("isLogin_manger"):
        # return render(request, "search_manager/smg_login.html")
        return HttpResponseRedirect("/admin")
    disk_state = Get_System().get_disk()
    ip = Get_System().get_ip()
    return render(request, "search_manager/index.html",
                  {"disk": disk_state, "ip": ip})


def charts(request):
    """
    渲染数据处理页面
    """
    if not request.session.get("isLogin_manger"):
        # return render(request, "search_manager/smg_login.html")
        return HttpResponseRedirect("/admin")
    disk_state = Get_System().get_disk()
    ip = Get_System().get_ip()
    return render(request, "search_manager/smg_charts.html",
                  {"disk": disk_state, "ip": ip})


def artical(request):
    """
    渲染文章页面
    """
    if not request.session.get("isLogin_manger"):
        # return render(request, "search_manager/smg_login.html")
        return HttpResponseRedirect("/admin")
    disk_state = Get_System().get_disk()
    ip = Get_System().get_ip()
    return render(request, "search_manager/smg_artical.html",
                  {"disk": disk_state, "ip": ip})


def get_artical(request):
    """
    获取用户反馈的信息
    POST 接受页面 初始化为 1
    :param request:
    :type request:
    :return: 用户名、类型、日期、状态
    :rtype: dict
    """
    if not request.session.get("isLogin_manger"):
        # return render(request, "search_manager/smg_login.html")
        return HttpResponseRedirect("/admin")
    page = request.POST.get("page")
    from searchapp.models import articlev2
    articals = articlev2.objects.all()
    total = len(articals)
    try:
        page = int(page)
    except BaseException:
        return HttpResponse(status=404)

    if page <= 0:
        return HttpResponse(status=404)

    articals = articlev2.objects.all()[(page-1)*10:page*10]
    artical_list = []
    for i in articals:
        artical_dict = {}
        artical_dict["name"] = i.name
        artical_dict["title"] = i.title
        artical_dict["id"] = i.id
        if i.flag == 0:
            artical_dict["flag"] = "未读"
        else:
            artical_dict["flag"] = "已读"
        artical_dict["date"] = i.getdate
        artical_list.append(artical_dict)
    return JsonResponse({"total":total,"artical_list":artical_list})

def get_artical_detial(request):
    """
    获取一片反馈的详细
    :param request:
    :type request:
    :return:
    :rtype:
    """
    if not request.session.get("isLogin_manger"):
        return HttpResponseRedirect("/admin")

    id = request.POST.get("id")
    from searchapp.models import articlev2
    user = articlev2.objects.get(id=id)
    if user.flag == 0:
        user.flag = 1
    user.save()
    return JsonResponse({"text":user.text})

def people(request):
    """
    获取people页面
    :param request:
    :type request:
    :return: people 页面 ip
    :rtype: json
    """
    if not request.session.get("isLogin_manger"):
        return HttpResponseRedirect("/admin")
    disk_state = Get_System().get_disk()
    ip = Get_System().get_ip()
    return render(request, "search_manager/smg_people.html",
                  {"disk": disk_state, "ip": ip})


def get_people(request):
    """
    获取用户的信息
    POST 接受页面 初始化为 1
    :param request:
    :type request:
    :return: 用户名、邮箱、状态
    :rtype: dict
    """
    if not request.session.get("isLogin_manger"):
        # return render(request, "search_manager/smg_login.html")
        return HttpResponseRedirect("/admin")
    from searchapp.models import search_user
    page = request.POST.get("page")
    try:
        page = int(page)
    except BaseException:
        return HttpResponse(status=404)

    if page <= 0:
        return HttpResponse(status=404)
    users = search_user.objects.all()
    total = len(users)
    users = users[(page - 1) * 10:page * 10]
    data_list = []
    for i in users:
        data_dict = {}
        data_dict["name"] = i.name
        data_dict["email"] = i.email
        if i.flag == 1:
            data_dict["flag"] = "已禁用"
        else:
            data_dict["flag"] = "正常"
        data_list.append(data_dict)
    return JsonResponse({"data_list": data_list, "total": total})


def change_state2people(request):
    """
    改变用户的状态
    :param request:
    :type request:
    :return:
    :rtype:
    """
    if not request.session.get("isLogin_manger"):
        return HttpResponseRedirect("/admin")
    name = request.POST.get("name")
    id = request.POST.get("id")
    from searchapp.models import search_user
    user = search_user.objects.get(name=name)
    if user.flag == 0:
        user.flag = 1
    else:
        user.flag = 0
    user.save()

    return JsonResponse({"id": id})


# 没用到可删除
def navbar(request):

    if not request.session.get("isLogin_manger"):
        return HttpResponseRedirect("/admin")
    disk_state = Get_System().get_disk()
    ip = Get_System().get_ip()
    return render(request, "search_manager/smg_navbar.html",
                  {"disk": disk_state, "ip": ip})

# 没用到可删除
def cards(request):
    if not request.session.get("isLogin_manger"):
        return HttpResponseRedirect("/admin")
    disk_state = Get_System().get_disk()
    ip = Get_System().get_ip()
    return render(request, 'search_manager/smg_cards.html',
                  {"disk": disk_state, "ip": ip})


def get_new_msg(request):
    """
    获取新的反馈
    """
    if not request.session.get("isLogin_manger"):
        return HttpResponse(status=404)
    from searchapp.models import articlev2
    msgs = articlev2.objects.filter(flag=0)
    data_list = []
    for a in msgs:
        msgs_dict = {}
        msgs_dict["id"] = a.id
        msgs_dict["name"] = a.name
        msgs_dict["text"] = a.text
        msgs_dict["date"] = a.getdate.strftime("%H:%M:%S")
        # a.flag = 1;
        data_list.append(msgs_dict)
    from mysite.tools.Class_get_system import Get_System
    my_system = Get_System()
    send_speed = my_system.get_net_speed()["send_speed"]
    recv_speed = my_system.get_net_speed()["recv_speed"]
    boot_time = time.strftime(
        "%H小时%M分%S秒",
        time.localtime(
            time.time() -
            my_system.get_boot_time() -
            8 *
            60 *
            60))
    return JsonResponse({"data_list": data_list,
                         "send_speed": send_speed,
                         "recv_speed": recv_speed,
                         "boot_time": boot_time})


def get_system_msg(request):
    """
    获取系统信息 cpu 和内存
    :param request:
    :type request:
    :return:
    :rtype:
    """
    if not request.session.get("isLogin_manger"):
        return HttpResponse(status=404)
    from mysite.tools.Class_get_system import Get_System
    my_system = Get_System()
    memory = my_system.get_memory()
    cpu = my_system.get_cpu()
    return JsonResponse({"cpu": cpu, "memory": memory})


def get_process(request):
    """
    获取进程
    """
    from mysite.tools.Class_get_system import Get_System
    my_system = Get_System()
    procress = my_system.get_process()
    procress = sorted(procress, key=lambda cpu: cpu["cpu_percent"])[-10:]
    for p in procress:
        p['create_time'] = time.strftime(
            "%Y-%m-%d %H:%M:%S",
            time.localtime(
                p['create_time']))
    procress.reverse()
    return JsonResponse({"procress": procress})


@csrf_exempt
def page_not_found(request):
    return render_to_response('404.html')


def get_data(request):
    """
    管理员对数据的处理
    :param request:
    :type request:
    :return:
    :rtype:
    """
    if not request.session.get("isLogin_manger"):
        return HttpResponse(status=404)
    msg = request.GET.get("msg", "")
    msg.strip()
    page = request.GET.get("page", 0)
    try:
        page = int(page)
    except BaseException:
        page = 1
    # 分析语法、错误处理、语法是否合法尚 均在底层实现 这里只做简单的处理,去掉最后一个;
    msgs = msg.split(";")
    if msgs[-1] == "":
        msgs.pop()
    res = ElasticSearch().search(msgs, page=page)
    tag = msg
    try:
        total = res["hits"]["total"]
        hits_list = []
        for hit in res["hits"]["hits"]:
            hits_dict = {}
            hits_dict["ip"] = hit["_source"]["ip"]
            # hits_dict["read"] = hit["_source"]["read"]
            hits_dict["server"] = hit["_source"]["server"]
            hits_dict["prowerd"] = hit["_source"]["prower"]
            hits_dict["title"] = hit["_source"]["title"]
            hits_dict["timestamp"] = hit["_source"]["timestamp"]
            hits_list.append(hits_dict)
        return JsonResponse({"page": page,
                             "total": total,
                             "tag": tag,
                             "all_hits": hits_list})
    except BaseException:
        return JsonResponse({"page": 0,
                             "total": 0,
                             "tag": tag,
                             "all_hits": None})


def delete_sr_data(request):
    """
    删除一条数据
    :param request:
    :type request:
    :return:
    :rtype:
    """
    if not request.session.get("isLogin_manger"):
        return HttpResponse(status=404)
    ip = request.POST.get("ip")
    res = ElasticSearch()
    if res.delete_data(ip):
        return JsonResponse({"info": 0})
    else:
        return JsonResponse({"info": 1})
