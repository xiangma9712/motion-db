from django.urls import path
from django.views.decorators.cache import cache_page
from django.conf import settings
from . import views

if settings.DEBUG:
    cache_time = 10
else:
    cache_time = 60 * 24 + 30

urlpatterns = [
    #path('set/', (cache_page(cache_time))(views.rand_set), name='random_set'),
    path('',(cache_page(cache_time))(views.rand_each), name='random'),
    path('set/', (cache_page(cache_time))(views.rand_asianset), name='random_set'),
]