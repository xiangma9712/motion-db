from django.shortcuts import render
from home.models import *
from accounts.models import Evaluator
from django.http import HttpResponseRedirect as redirect
from django.http import Http404

def index(request):
    if request.method == 'POST':
        dir = upload(request)
        id = Motion.objects.get(id=dir['id']).meta_id
        fine = dir['fine']
        if not fine:
            return redirect('/motions/?id='+str(id)+'&msg=2')
        if fine:
            return redirect('/motions/?id='+str(id)+'&msg=1')

    if not "id" in request.GET:
        raise Http404()

    id = request.GET.get("id")
    motion_list = Motion.objects.filter(meta_id=id)
    if len(motion_list) == 0:
        raise Http404()
        
    context = {
        'motion_list' : motion_list,
        'theme_list' : Theme.objects.filter(deprecated=False).order_by('theme_str'),
        'msg_id' : request.GET.get("msg"),
    }

    return render(request, "motions/each.html", context)

def upload(request):
    id = int(request.POST.get("id"))
    fine_dir = {
        'fine' : True,
        'id' : id,
    }
    motion = Motion.objects.get(id=id)
    
    if request.POST.get("which") == "theme":
        p_theme = request.POST.get("p-theme","")
        s_theme = request.POST.get("s-theme","")
        try:
            theme_top = Theme.objects.get(id=p_theme).theme_str
        except ValueError:
            theme_top = ""
        try:
            theme_add = Theme.objects.get(id=s_theme).theme_str
        except ValueError:
            theme_add = ""
        motion.theme_top = theme_top
        motion.theme_add = theme_add
        motion.save()
        return fine_dir
    
    if request.POST.get("which") == "info":
        info = request.POST.get("info","").replace("\r\n"," ").replace("\n"," ")
        motion.info_text = info
        motion.save()
        return fine_dir
    
    if request.POST.get("which") == "eval":
        user = request.user
        evaluated = []
        try:
            evaluated = user.eval.evaluated_list
        except:
            Evaluator.objects.create(user=user,evaluated_list=[])
        eval = float(request.POST.get("eval"))
        if not id in user.eval.evaluated_list:
            user.eval.evaluated_list.append(id)
            user.eval.save()
            motion.record_evaluation(eval,user.id)
        else:
            motion.change_evaluation(eval,user.id)
        return fine_dir
    
    motion_text = request.POST.get("motion").replace("\r\n"," ").replace("\n"," ")    
    if len(motion_text.split()) < 3 or len(motion_text) < 12:
        dir = {
            'fine' : False,
            'id' : id,
        }
        return dir
    
    motion.motion_text = motion_text
    motion.save()
    return fine_dir

def ranking(request):
    min = 3
    try:
        min = Setting.objects.get(name='ranking').int
    except Setting.DoesNotExist:
        pass
    
    motions = Motion.objects.filter(copy_num__gte=min).order_by('copy_num').reverse()
    context = {'motion_list' : motions}
    return render(request,"motions/ranking.html",context)