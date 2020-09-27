from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register('motion', MotionViewSet)
router.register('copy', CopyViewSet)
router.register('set',AsianSetViewSet)
urlpatterns = [
    url('', include(router.urls)),
]
