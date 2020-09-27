from django.shortcuts import render
from django.template.response import SimpleTemplateResponse
from home.models import Motion, Meta, Tournament,Theme, Round
from django.http import HttpResponseRedirect as redirect
from . import scrape_funcs as sf
import datetime

def build(request):
    errorlog = False
    if request.method == "POST":
        dir = buildInDB(request)
        fine = dir['fine']
        if fine:
            id = dir['id']
            url = "/motions/?id=" + str(id)
            exist = dir['exist']
            if exist:
                url += "&msg=3"
            else:
                url += "&msg=1"
            return redirect(url)
        errorlog = True

    year = datetime.datetime.now().year
    round_list = Round.objects.all()
    theme_list = Theme.objects.filter(deprecated=False).order_by('theme_str')
    tour_list = Tournament.objects.filter(ongoing=True)
    meta_list = Meta.objects.all()
    meta_json = ",".join(list(map(lambda m : m.to_json(),meta_list)))
    tournament_json = ",".join(list(map(lambda t : t.to_json(),tour_list)))

    context = {
        'meta_json' : meta_json,
        'round_list' : round_list,
        'tournament_json' : tournament_json,
        'theme_list' : theme_list,
        'year' : year,
        'errorlog' : errorlog,
    }

    return render(request,"upload/motion.html",context)

def mainpage(request):
    if request.method == "POST":
        url = build_url(request)
        return redirect(url)

    year = datetime.datetime.now().year
    tour_list = Tournament.objects.filter(ongoing=True)
    tournament_json = ",".join(list(map(lambda t : t.to_json(),tour_list)))

    context = {
        'tournament_json' : tournament_json,
        'year' : year,
    }

    return render(request,"upload/main.html",context)

def build_url(request):
    tour_name = request.POST.get("tour_name")
    tour_id = Tournament.objects.get(tournament_name=tour_name).id
    year = request.POST.get("year")
    switcher = request.POST.get("method")
    add = "?ti=" + str(tour_id) + "&year=" + year

    if switcher == 1:
        return "/upload/write/" + add
    else:
        return "/upload/scrape/" + add

def write(request):
    errorlog = False
    if request.method == "POST":
        dir = buildInDB(request)
        fine = dir['fine']
        if fine:
            id = dir['id']
            url = "/motions/?id=" + str(id)
            exist = dir['exist']
            if exist:
                url += "&msg=3"
            else:
                url += "&msg=1"
            return redirect(url)
        errorlog = True

    year = request.GET.get("year")
    tour_id = request.GET.get("ti")
    round_list = Round.objects.all()
    theme_list = Theme.objects.filter(deprecated=False).order_by('theme_str')
    meta_list = Meta.objects.filter(tournament_id=tour_id,year=year)
    meta_json = ",".join(list(map(lambda m : m.to_json(),meta_list)))

    context = {
        'meta_json' : meta_json,
        'round_list' : round_list,
        'tournament' : Tournament.objects.get(id=tour_id),
        'theme_list' : theme_list,
        'year' : year,
        'errorlog' : errorlog,
    }

    return render(request,"upload/write.html",context)

def scrape(request):
    year = request.GET.get("year")
    tour_id = request.GET.get("ti")
    tournament = Tournament.objects.get(id=tour_id)
    is_asian = (tournament.style == 1)
    
    if request.method == "POST":
        url = request.POST.get("url")
        motion_dir = sf.scrape(url, is_asian)
        return after_scrape(motion_dir,tour_id,year)
    
    context = {
        'tournament' : tournament,
        'year' : year,
        'is_asian' : is_asian,
    }
    return render(request,"upload/scrape.html",context)

def buildInDB(request):
    exist_id = int(request.POST.get("exist"))
    if not exist_id == 0:
        dir = {
            'id' : exist_id,
            'exist' : True,
            'fine' : True,
        }
        return dir

    try:
        round_id = int(request.POST.get("round"))
        round = Round.objects.get(id=round_id).round_str
    except (ValueError, NameError, TypeError):
        dir = {
            'fine' : False,
        }
        return dir

    tour_name = request.POST.get("tournament")
    tour_id = Tournament.objects.get(tournament_name=tour_name).id
    style = Tournament.objects.get(tournament_name=tour_name).style
    year = int(request.GET.get("year"))

    #meta check
    check = Meta.objects.filter(tournament_id=tour_id,year=year,round=round)
    if len(check) != 0:
        dir = {
            'id' : check[0].id,
            'exist' : True,
            'fine' : True,
        }
        return dir

    #motion check
    motion_text = []
    motion_text.append(request.POST.get("motion").replace("\r\n"," ").replace("\n"," "))
    if style == 1:
        motion_text.append(request.POST.get("motion2").replace("\r\n"," ").replace("\n"," "))
        motion_text.append(request.POST.get("motion3").replace("\r\n"," ").replace("\n"," "))

    for motion in motion_text:
        if len(motion.split()) < 3 or len(motion) < 12:
            dir = {
                'fine' : False,
            }
            return dir

    meta_id = Meta.objects.order_by('id').last().id + 1
    new_meta = Meta(id=meta_id,tournament_id=tour_id,year=year,round=round,style=style)
    new_meta.save()

    info = [request.POST.get("info","").replace("\r\n"," ").replace("\n"," ")]
    p_theme = [request.POST.get("p-theme","")]
    s_theme = [request.POST.get("s-theme","")]
    until = 1
    if style == 1:
        info.append(request.POST.get("info2").replace("\r\n"," ").replace("\n"," "))
        p_theme.append(request.POST.get("p-theme2"))
        s_theme.append(request.POST.get("s-theme2"))
        info.append(request.POST.get("info3").replace("\r\n"," ").replace("\n"," "))
        p_theme.append(request.POST.get("p-theme3"))
        s_theme.append(request.POST.get("s-theme3"))
        until = 3
    for num in range(0,until):
        build_dir = {
            'motion' : motion_text[num],
            'info' : info[num],
            'p_theme' : p_theme[num],
            's_theme' : s_theme[num],
            'meta_id' : meta_id,
            'style' : style,
        }
        buildMotion(build_dir)
    dir = {
        'id' : meta_id,
        'exist' : False,
        'fine' : True,
    }
    return dir

def buildMotion(dir):
    motion_text = dir['motion']
    info = dir['info']
    p_theme = dir['p_theme']
    s_theme = dir['s_theme']
    meta = dir['meta_id']
    style = dir['style']
    try:
        theme_top = Theme.objects.get(id=p_theme).theme_str
    except:
        theme_top = ""
    try:
        theme_add = Theme.objects.get(id=s_theme).theme_str
    except:
        theme_add = ""
    motion_id = Motion.objects.order_by('id').last().id + 1
    Motion.objects.create(id=motion_id,motion_text=motion_text,info_text=info,theme_top=theme_top,theme_add=theme_add,meta_id=meta,style=style)

    return

def after_scrape(motion_dir,tour_id,year):
    meta_list = []
    style = Tournament.objects.get(id=tour_id).style
    meta_id = Meta.objects.order_by("id").last().id + 1
    motion_id = Motion.objects.order_by("id").last().id + 1
    to_del = []
    for r,m in motion_dir.items():
        count = Meta.objects.filter(tournament_id = tour_id, round=r, year=year).count()
        if not count == 0:
            to_del.append(r)
    
    for each in to_del:
        del motion_dir[each]
    
    for r,m in motion_dir.items():
        Meta.objects.create(id=meta_id,year=year,tournament_id=tour_id,round=r,style=style)
        if not style == 1:
            motion_text = m[0]
            info =  m[1]
            Motion.objects.create(id=motion_id,motion_text=motion_text,info_text=info,meta_id=meta_id,style=style)
            motion_id += 1
        else:
            for each in m:
                motion_text = each[0]
                info = each[1]
                Motion.objects.create(id=motion_id,motion_text=motion_text,info_text=info,meta_id=meta_id,style=style)
                motion_id += 1
        meta_list.append(meta_id)
        meta_id += 1
    
    motions = Motion.objects.filter(meta_id__in = meta_list)
    context = {"motion_list" : motions}
    t = SimpleTemplateResponse("upload/scrape_result.html",context)
    return t.render()
                
        
