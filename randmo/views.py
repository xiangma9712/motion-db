from django.shortcuts import render
from home.models import Motion,Meta,Tournament, Setting, AsianSet
from django.http import Http404
import datetime

def rand_set(request):
    tournament_list = Tournament.objects.all().order_by('id')
    year = datetime.datetime.now().year
    year_range = Setting.objects.get(name="random").int
    year_from = year - year_range + 1
    meta_list = Meta.objects.filter(style=1, year__gte=year_from)
    motion_list = Motion.objects.filter(style=1)
    motion_json = ",".join(list(map(lambda m : m.to_json_2(),motion_list)))
    
    meta_list_2 = list(meta_list.values_list('id', flat=True))
    set_list = list(map(lambda m: motion_list.filter(meta=m),meta_list))

    context = {
        'set_list' : set_list,
        'meta_list' : meta_list_2,
        'motion_json' : motion_json,
    }
    template = 'randmo/random_asian.html'    
    
    return render(request, template, context)

def rand_asianset(request):
    year = datetime.datetime.now().year
    year_range = Setting.objects.get(name="random").int
    year_from = year - year_range + 1
    set_list = AsianSet.objects.filter(year__gte=year_from)
    ids = ",".join(list(map(lambda x:str(x.id),set_list)))
    context = {
        'set_list' : set_list,
        'id_list' : ids,
    }
    template = 'randmo/random_asianset.html'
    return render(request, template, context)

def rand_each(request):
    year = datetime.datetime.now().year
    try:
        year_range = Setting.objects.get(name="random").int
    except:
        year_range = 3
        
    year_from = year - year_range
    style_str = "All"
    motion_list = Motion.objects.filter(year__gte=year_from)
    if "st" in request.GET:
        style = request.GET.get("st")
        motion_list = motion_list.filter(style=style)
        meta_list = Meta.objects.filter(style=style, year__gte=year_from)
        if style == '0':
            style_str = "BP"
            year_from += 1
        elif style == '2':
            style_str = "NA"
        else:
            raise Http404()
    
    motion_id_json = []
    for motion in motion_list:
        motion_id_json.append(motion.id)        
    
    context = {
        'motion_id_json' : motion_id_json,
        'motion_list' : motion_list,
        'style_str' : style_str,
    }
    template = 'randmo/random2.html'
    
    return render(request, template, context)
    