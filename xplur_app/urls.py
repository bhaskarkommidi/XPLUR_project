#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 14:04:16 2019

@author: sambhav
"""
from django.conf.urls import url
from .views import UserRegistrationView,UserLoginView,Products,Product_create,Product_update,Product_delete
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Swagger API')


urlpatterns = [
	url(r'^$', schema_view),
    url(r'^signup', UserRegistrationView.as_view()),
    url(r'^signin', UserLoginView.as_view()),
    url(r'^products', Products),
    url(r'^product_create/$', Product_create),
    url(r'^product_update/(?P<product_id>[0-9]+)/$', Product_update),
    url(r'^product_delete/(?P<product_id>[0-9]+)/$', Product_delete),
    ############################################
    # url(r'^products', Products.as_view()),
    # url(r'^product_create', Product_create.as_view()),
    
    ]