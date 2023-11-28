from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('profile', views.CustomerViewSet)
router.register('professional', views.ArtisanPortfolioViewSet)
router.register('category', views.ArtisanCategoryViewSet)


urlpatterns =  router.urls

