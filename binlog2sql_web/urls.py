"""
URL configuration for binlog2sql_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import binlog_form, run_binlog2sql,index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('run-binlog2sql/', run_binlog2sql, name='run_binlog2sql'),
    path('binlog-form/', binlog_form, name='binlog_form'),
    path('', index, name='index'),
]


