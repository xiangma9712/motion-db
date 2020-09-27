from django.shortcuts import render
from home.models import Motion,Tournament,Round,Theme,Meta
from django.http import HttpResponseRedirect as redirect
from django.db.models import Q
import datetime

def search(request):
    if "s1" in request.POST:
        url = result_url(request)
        return redirect(url)
        
    theme_list = Theme.objects.all().order_by('theme_str')
    round_list = Round.objects.all()
    tournament_list = Tournament.objects.all().order_by('id')
    year = datetime.datetime.now().year

    tournament_json = ",".join(list(map(lambda t : t.to_json(),tournament_list)))
    context = { 'theme_list' : theme_list,
                'round_list' : round_list,
                'year' : year,
                'tournament_json' : tournament_json,}
    return render(request, 'search/top.html', context)

def result(request):
    url = request.GET
    tournament_list = []
    to_all = True
    year = datetime.datetime.now().year

    #大会の抽出
    if "tn" in url:
        tn = url.get("tn")
        tournament_list = [Tournament.objects.get(tournament_name=tn)]
        to_all = False
    else:
        tournament_list = Tournament.objects.all()
        tl = url.get("tl")
        st = url.get("st")
        if not tl == None:
             tournament_list = tournament_list.filter(level = tl)
             to_all = False
        if not st == None:
            tournament_list = tournament_list.filter(style = st)
            to_all = False
    to_matched = list(map(lambda t : t.id,tournament_list))

    #メタの抽出
    yf = url.get("yf",2000)
    yt = url.get("yt",year)
    if to_all:
        motion_list = Motion.objects.all()
    else:
        motion_list = Motion.objects.filter(tournament_id__in=to_matched)
    if "ip" in url:
        round_list = Round.objects.filter(is_preliminary=bool(int(url.get("ip"))))
        rounds = list(map(lambda r: r.id,round_list))
        motion_list = motion_list.filter(round__in=rounds)
    if not yf == 2000:
        motion_list = motion_list.filter(year__gte=yf)
    if not yt == year:
        motion_list = motion_list.filter(year__lte=yt)
        
    if "kw" in url:
        kw = url.get("kw")
        motion_list = motion_list.filter(motion_text__contains=kw)
        motion_all = False
    if "ti" in url:
        theme = Theme.objects.get(id = url.get("ti"))
        motion_list = motion_list.filter(Q(theme_top = theme.theme_str)|Q(theme_add = theme.theme_str))
        motion_all = False

    context = { 'motion_list' : motion_list,}
    return render(request, 'search/result.html', context)

def result_url(request):
    url = "/search/result/?"
    swap_pair = {
        "s1" : "st",
        "s2" : "tl",
        "s4" : "ip",
        "KWD" : "kw",
        "theme" : "ti"
    }
    additions = []
    for k,v in swap_pair.items():
        if k in request.POST and not request.POST.get(k) == "null":
            additions.append(v + "=" + request.POST.get(k))
    
    url += "&".join(additions)
    return url