from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('category', views.CategoryViewSet)
router.register('post', views.PostViewSet)
router.register('tag', views.TagViewSet)


app_name = 'user'

urlpatterns = [
    path('', include(router.urls)),
]