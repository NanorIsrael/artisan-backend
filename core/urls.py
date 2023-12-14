from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('profile', views.CustomerViewSet)
router.register('artisan', views.ArtisanPortfolioViewSet)
router.register('category', views.ArtisanCategoryViewSet)
router.register('address', views.AddressViewSet)
router.register('customer', views.ProfilePhotoViewSet)
router.register('rating', views.ArtisanRatingViewset)
router.register('review', views.ArtisanReviewViewset)


urlpatterns =  router.urls

