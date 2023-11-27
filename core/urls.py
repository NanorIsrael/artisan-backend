from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('customer', views.CustomerViewSet)


urlpatterns =  router.urls
