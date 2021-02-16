from django.urls import path, include
from rest_framework.routers import DefaultRouter

from meme import views

router = DefaultRouter()
router.register('memes', views.MemeViewSet)

app_name = 'meme'

urlpatterns = [
    path('', include(router.urls))
]