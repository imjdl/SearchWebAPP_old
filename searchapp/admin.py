# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import search_user
admin.site.register(search_user)
admin.site.site_header = "SearchApp 后台管理系统"
admin.site.site_title = "SearchApp 网络空间搜索引擎后台"