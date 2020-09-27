from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('message/', views.msg, name='msg'),
    path('privacy/',views.privacy,name="privacy"),
    path('contact/',views.contact,name="contact"),
]
