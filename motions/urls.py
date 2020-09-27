from django.urls import path
from django.views.decorators.cache import cache_page
from django.conf import settings
from . import views

if settings.DEBUG:
    cache_time = 10
else:
    cache_time = 60 * 24 + 30

urlpatterns = [
    #path('past/', views.index, name='index'),
    path('',views.each,name='each'),
    path('set/', views.set, name='set'),
    path('ranking/', (cache_page(cache_time))(views.ranking), name='ranking'),
    path('theme/',views.classify,name='classify'),
]