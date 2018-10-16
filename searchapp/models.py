# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Create your models here.

class search_user(models.Model):
    """
    搜索引擎用户的定义
    """
    name = models.CharField(max_length=16)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=16)
    flag = models.IntegerField()
    def __str__(self):
        return self.name + ":" +self.email

class ports_data(models.Model):
    """
    定义数据段
    """
    ip = models.CharField(max_length=45,primary_key=True)
    os = models.CharField(max_length=100)
    hostname = models.CharField(max_length=100)
    ports = models.TextField(max_length=100)
    getdate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.ip

class articlev2(models.Model):
    """
    定义反馈的数据
    """
    name = models.CharField(max_length=16)
    title = models.CharField(max_length=16)
    text = models.TextField(max_length=100)
    flag = models.IntegerField()
    getdate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name + ":" +self.title