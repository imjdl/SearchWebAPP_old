from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.admin, name="admin"),
    url(r"^login_manager/$", views.login_manager, name="login_manager"),
    url(r'^manager/$', views.index, name="manager"),
    url(r'^charts/$', views.charts, name="charts"),
    url(r'^peoples/$', views.people, name="people"),
    url(r'^artical/', views.artical, name="artical"),
    url(r'^navbar/$', views.navbar, name="navbar"),
    url(r'^cards/$', views.cards, name="cards"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^getnewmsg/', views.get_new_msg, name="getnewmsg"),
    url(r'^getsystemmsg/', views.get_system_msg, name="getsystemmsg"),
    url(r'^getproses/', views.get_process, name="getprocess"),
    url(r'^getsearchdata/', views.get_data, name="getsearchdata"),
    url(r"^delete_searchdata/", views.delete_sr_data, name="delete_searhe_data"),
    url(r'^get_prople/', views.get_people, name="get_people"),
    url(r'^chang_state_people', views.change_state2people, name="chang_statw2people"),
    url(r'^get_artical/', views.get_artical, name="get_artical"),
    url(r"^get_artical_detial", views.get_artical_detial, name="get_artical_detial"),
]
