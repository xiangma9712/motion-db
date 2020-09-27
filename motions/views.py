from django.shortcuts import render
from home.models import *
from accounts.models import Evaluator
from django.http import HttpResponseRedirect as redirect
from django.http import Http404

def each(request):
    if not "id" in request.GET:
        raise Http404()

    id = int(request.GET.get("id"))

    if request.method == 'POST':
        dir = upload(request)
        fine = dir['fine']
        if not fine:
            return redirect('/motions/?id='+str(id)+'&msg=2')
        if fine:
            return redirect('/motions/?id='+str(id)+'&msg=1')
    motion = Motion.objects.get(id=id)
    if motion == None:
        raise Http404()

    score = 5
    if request.user.is_authenticated:
        score = motion.past_evaluation(request.user.id)

    context = {
        'motion' : motion,
        'theme_list' : Theme.objects.filter(deprecated=False).order_by('theme_str'),
        'msg_id' : request.GET.get("msg"),
        'score' : score,
    }

    return render(request, "motions/each_new.html", context)

def set(request):
    if not "id" in request.GET:
        raise Http404()

    id = int(request.GET.get("id"))
    if request.method == 'POST':
        dir = upload(request)
        fine = dir['fine']
        if not fine:
            return redirect('/motions/set/?id='+str(id)+'&msg=2')
        if fine:
            return redirect('/motions/set/?id='+str(id)+'&msg=1')

    motion_set = AsianSet.objects.get(id=id)
    motion_list = [motion_set.one,motion_set.two,motion_set.three]
    if motion_set == None:
        raise Http404()

    context = {
        'motion_set' : motion_set,
        'motion_list': motion_list,
        'theme_list' : Theme.objects.filter(deprecated=False).order_by('theme_str'),
        'msg_id' : request.GET.get("msg"),
    }

    return render(request, "motions/set.html", context)

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
    if not "type" in request.GET:
        raise Http404()

    if request.GET.get("type") == "copy":
        min = 3
        try:
            min = Setting.objects.get(name='ranking').int
        except Setting.DoesNotExist:
            pass

        motions = Motion.objects.filter(copy_num__gte=min).order_by('copy_num').reverse()
        description = "Most copied motions in the last 2 manths"
    elif request.GET.get("type") == "fairness":
        max = 0.5
        try:
            max = Setting.objects.get(name='fairness_rank').int
        except Setting.DoesNotExist:
            pass
        motions = Motion.objects.filter(fairness__lte=max).order_by('fairness')
        description = "Fairest motions based on users' vote"

    context = {
        'motion_list' : motions,
        'description' : description,
        'type' : request.GET.get("type")
    }
    return render(request,"motions/ranking.html",context)

def classify(request):
    motion = Motion.objects.filter(theme_top="",theme_add="").order_by("id").last()
    if request.method == 'POST':
        dir = upload(request)
        return redirect('/motions/theme/')

    context = {
        "motion":motion,
        'theme_list' : Theme.objects.filter(deprecated=False).order_by('theme_str'),
    }

    return render(request,"motions/classify.html",context)
