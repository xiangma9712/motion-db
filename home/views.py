from django.shortcuts import render
from .models import Motion,Meta,Tournament, Message, Theme
from django.template.response import SimpleTemplateResponse
from django.db.models import Q
from django.http import Http404

def home(request):
    tournament_list = Tournament.objects.all().order_by('level')
    count = Motion.objects.count()
    messages = Message.objects.all().order_by('id')
    data = []
    for tour in tournament_list:
        each = Motion.possession(tour)
        data.append(each)
    theme_list = Theme.objects.all()
    dict = []
    for theme in theme_list:
        theme_str = theme.theme_str
        num = Motion.objects.filter(Q(theme_top = theme_str)|Q(theme_add = theme_str)).count()
        url = "/search/result/?ti=" + str(theme.id)
        each = {'str':theme_str,'num':num, 'url':url}
        dict.append(each)
    dir = {
        'data' : data,
        'count' : count,
        'msg' : messages,
        'dict' : dict,
    }
    return render(request, "home/coverage.html",dir)

def msg(request):
    if not 'id' in request.GET:
        raise Http404()
    id = int(request.GET.get("id"))
    try:
        message = Message.objects.get(id=id)
    except Message.DoesNotExist:
        raise Http404()
    
    before = Message.objects.filter(id__lt=id).last()
    next = Message.objects.filter(id__gt=id).first()
    
    
    lines = message.body.split("<br>")
    context = {
        'message' : message,
        'before'  : before,
        'next'    : next,
        'lines'   : lines,
    }
    return render(request,"home/message.html",context)

def privacy(request):
    t = SimpleTemplateResponse("fixedpage/privacy.html")
    return t.render()

def contact(request):
    t = SimpleTemplateResponse("fixedpage/contact.html")
    return t.render()