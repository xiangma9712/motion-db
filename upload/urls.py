from django.urls import path
from . import views

urlpatterns = [
    path('',views.mainpage, name='main'),
    path('write/',views.write, name='write'),
    path('scrape/',views.scrape, name='scrape'),
]
