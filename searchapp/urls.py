from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^search/', views.getdata, name="search_data_process"),
    url(r'^detial/', views.detial, name="data_info_detial"),
    url(r"^login/", views.ajax_process, name="login_data"),
    url(r'^logout/', views.logout_process, name="logout_data"),
    url(r"^code/", views.create_code, name="create_code"),
    url(r"^email/", views.sendEmail, name="send_email"),
    url(r'^register/', views.register_process, name="reg_data"),
    url(r"^forget/", views.forgetpaswd, name="forget"),
    url(r"^change/", views.changepaswd, name="change"),
    url(r'^getport/', views.get_scanport, name="get_port"),
    url(r'^dataanl/$', views.dataanal ,name="dataanl"),
    url(r'^help/$', views.help, name="help"),
    url(r'^about/$', views.about, name="about"),
    url(r"^contact/$", views.contact, name="contact"),
    url(r"^webdata/", views.getwebdata, name="webdata"),
    url(r"^submit_sugest/", views.get_contact, name="sugest"),
    # -------------------分割线------------------------------
    # url(r'^sum_post/', views.sum_post,name="sum_post"),
    # url(r'^sum/', views.sum,name="sum"),
    # url(r'^get_sum/', views.get_sum, name="get_sum"),
    # url(r'^resp/', views.hello, name="hello"),
    # url(r'^add/(\d+)/(\d+)/$', views.jump, name="add"),
    # url(r'^new_add/(\d+)/(\d+)/$', views.sum2, name="add2"),
]
