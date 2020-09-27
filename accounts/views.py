from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from . import forms
from .models import Evaluator
from home.models import Motion
from django.http import HttpResponseRedirect as redirect
from django.shortcuts import render
import random

class MyLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "accounts/login.html"

class MyLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "accounts/logout.html"

class UserCreateView(CreateView):
    form_class = forms.CreateForm
    template_name = "accounts/create.html"
    success_url = reverse_lazy("login")

def evaluate(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('/accounts/login/?next=/accounts/evaluate/')
        
    evaluated = []
    try:
        evaluated = user.eval.evaluated_list
    except:
        Evaluator.objects.create(user=user,evaluated_list=[])

    if request.method == 'POST':
        eval = float(request.POST.get("eval"))
        motion_id = int(request.POST.get("motion-id"))
        user.eval.evaluated_list.append(motion_id)
        user.eval.save()
        Motion.objects.get(id=motion_id).record_evaluation(eval,user.id)
        return redirect('/accounts/evaluate/')

    count = Motion.objects.all().count()
    start = int(count * 0.85)
    target = None
    while True:
        rand_idx = random.randint(start,count)
        target = Motion.objects.get(id=rand_idx)
        if not target.id in evaluated:
            break

    context = {"target" : target}
    return render(request,"accounts/evaluate.html",context)
