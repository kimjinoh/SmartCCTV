"""ahyun2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include
from . import views, api
from rest_framework import routers

router = routers.DefaultRouter()
router.register('user', api.cctvViewSet)
router.register('people',api.peopleViewSet)
router.register('detect', api.detectViewSet)
router.register('heatmap',api.heatmapViewSet)

urlpatterns = [
    url('', include(router.urls)),
    #path('create/', views.post_create, name='create'),
]
