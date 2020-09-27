from django.shortcuts import render
from django.template.response import SimpleTemplateResponse
from home.models import Motion, AsianSet, Tournament,Theme, Round
from django.http import HttpResponseRedirect as redirect
from . import scrape_funcs as sf
import datetime

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
    switcher = int(request.POST.get("method"))
    add = "?ti=" + str(tour_id) + "&year=" + year

    if switcher == 1:
        return "/upload/write/" + add
    else:
        return "/upload/scrape/" + add

def write(request):
    errorlog = False
    tour_id = request.GET.get("ti")
    tournament = Tournament.objects.get(id=tour_id)
    style = Tournament.style
    if request.method == "POST":
        dir = buildInDB(request)
        fine = dir['fine']
        if fine:
            id = dir['id']
            if style == 1:
                url = "/motions/?set=" + str(id)
            else:
                url = "/motions/?id=" + str(id)
            exist = dir['exist']
            if exist:
                url += "&msg=3"
            else:
                url += "&msg=1"
            return redirect(url)
        errorlog = True

    year = request.GET.get("year")
    round_list = Round.objects.all()
    theme_list = Theme.objects.filter(deprecated=False).order_by('theme_str')
    if style == 2:
        set_list = AsianSet.objects.filter(tournament_id=tour_id,year=year)
        meta_json = ",".join(list(map(lambda m : m.to_json(),set_list)))
    else:
        motion_list = Motion.objects.filter(tournament_id=tour_id,year=year)
        meta_json = ",".join(list(map(lambda m : m.to_json(),motion_list)))

    context = {
        'meta_json' : meta_json,
        'round_list' : round_list,
        'tournament' : tournament,
        'theme_list' : theme_list,
        'year' : year,
        'errorlog' : errorlog,
    }

    return render(request,"upload/write_2.html",context)

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

def get_refined(request,str):
    return request.POST.get(str,"").replace("\r\n"," ").replace("\n"," ")

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
    except (ValueError, NameError, TypeError):
        dir = {
            'fine' : False,
        }
        return dir

    tour_name = request.POST.get("tournament")
    tour_id = Tournament.objects.get(tournament_name=tour_name).id
    style = Tournament.objects.get(tournament_name=tour_name).style
    if style == 1:
        return buildInDB_asian(request)

    year = int(request.GET.get("year"))

    #meta check
    check = Motion.objects.filter(tournament_id=tour_id,year=year,round_id=round_id)
    if len(check) != 0:
        dir = {
            'id' : check[0].id,
            'exist' : True,
            'fine' : True,
        }
        return dir

    #motion check
    motion_text = get_refined(request,"motion")
    if len(motion_text.split()) < 3 or len(motion_text) < 12:
        dir = {
            'fine' : False,
        }
        return dir

    info = get_refined(request,"info")
    theme_top = get_refined(request,"p-theme")
    theme_add = get_refined(request,"s-theme")
    motion_id = Motion.objects.order_by('id').last().id + 1
    Motion.objects.create(id=motion_id,
        motion_text=motion_text,
        info_text=info,
        theme_top=theme_top,
        theme_add=theme_add,
        style=style,
        tournament_id=tour_id,
        round_id = round_id,
        year = year
        )
    dir = {
        'id' : motion_id,
        'exist' : False,
        'fine' : True,
    }
    return dir

def buildInDB_asian(request):
    tour_name = request.POST.get("tournament")
    tour_id = Tournament.objects.get(tournament_name=tour_name).id
    year = int(request.GET.get("year"))

    #meta check
    check = AsianSet.objects.filter(tournament_id=tour_id,year=year,round_id=round_id)
    if len(check) != 0:
        dir = {
            'id' : check[0].id,
            'exist' : True,
            'fine' : True,
        }
        return dir

    #motion check
    motion_text = [get_refined(request,"motion"),get_refined(request,"motion2"),get_refined(request,"motion3")]
    for motion in motion_text:
        if len(motion.split()) < 3 or len(motion) < 12:
            dir = {
                'fine' : False,
            }
            return dir

    asianset_id = AsianSet.objects.order_by('id').last().id + 1


    info = [get_refined(request,"info"),get_refined(request,"info2"),get_refined(request,"info3")]
    theme_top = [get_refined(request,"p-theme"),get_refined(request,"p-theme2"),get_refined(request,"p-theme3")]
    theme_add = [get_refined(request,"s-theme"),get_refined(request,"s-theme2"),get_refined(request,"s-theme3")]
    motion_id = Motion.objects.order_by('id').last().id
    for num in range(0,3):
        motion_id += 1
        Motion.objects.create(id=motion_id,
            motion_text=motion_text[num],
            info_text=info[num],
            theme_top=theme_top[num],
            theme_add=theme_add[num],
            style=style,
            tournament_id=tour_id,
            round_id = round_id,
            year = year
        )

    AsianSet.objects.create(id=asianset_id,
        tournament_id=tour_id,
        round_id = round_id,
        year = year,
        one_id = motion_id - 2,
        two_id = motion_id - 1,
        three_id = motion_id
    )

    dir = {
        'id' : asianset_id,
        'exist' : False,
        'fine' : True,
    }
    return dir

def after_scrape(motion_dir,tour_id,year):
    motion_id_list = []
    style = Tournament.objects.get(id=tour_id).style
    set_id = AsianSet.objects.order_by("id").last().id + 1
    motion_id = Motion.objects.order_by("id").last().id + 1
    to_del = []
    for r,m in motion_dir.items():
        try:
            round = Round.objects.get(round_str=r)
            if not style == 1:
                count = Motion.objects.filter(tournament_id = tour_id, round=round, year=year).count()
            else:
                count = AsianSet.objects.filter(tournament_id = tour_id, round=round, year=year).count()
        except:
            count = 1
        if not count == 0:
            to_del.append(r)

    for each in to_del:
        del motion_dir[each]

    for r,m in motion_dir.items():
        round_id = Round.objects.get(round_str=r).id
        Meta.objects.create(id=meta_id,year=year,tournament_id=tour_id,round_id=round_id,style=style)
        if not style == 1:
            motion_text = m[0]
            info =  m[1]
            Motion.objects.create(id=motion_id,
                motion_text=motion_text,
                info_text=info,
                style=style,
                tournament_id=tour_id,
                round_id = round_id,
                year = year
            )
            motion_id_list.append(motion_id)
            motion_id += 1
        else:
            for each in m:
                motion_text = each[0]
                info = each[1]
                Motion.objects.create(id=motion_id,
                    motion_text=motion_text,
                    info_text=info,
                    style=style,
                    tournament_id=tour_id,
                    round_id = round_id,
                    year = year
                )
                motion_id_list.append(motion_id)
                motion_id += 1
            AsianSet.objects.create(id=set_id,
                year=year,
                tournament_id=tour_id,
                round_id=round_id,
                one_id = motion_id - 2,
                two_id = motion_id - 1,
                three_id = motion_id
            )
            set_id += 1

    motions = Motion.objects.filter(id__in = motion_id_list)
    context = {"motion_list" : motions}
    t = SimpleTemplateResponse("upload/scrape_result.html",context)
    return t.render()
