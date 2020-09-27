from django.shortcuts import render
from home.models import Tournament, Meta, Theme, Motion
from django.http import HttpResponseRedirect as redirect
from django.db.models import Q
from django.http import Http404

def index(request):
    if not "id" in request.GET:
        return render(request, "motions/top.html")

    id = request.GET.get("id")
    try:
        tournament = Tournament.objects.get(id=id)
    except Tournament.DoesNotExist:
        raise Http404()
    style = tournament.style
    style_str = ""
    if style == 0:
        style_str = "BP"
    elif style == 1:
        style_str = "Asian"
    elif style == 2:
        style_str = "NA"
    level = tournament.level
    level_str = ""
    if level == 0:
        level_str = "Rookie"
    elif level == 1:
        level_str = "Domestic"
    elif level == 2:
        level_str = "International"
    elif level == 3:
        level_str = "Pro-Am"
    
    meta_list = Meta.objects.filter(tournament_id = id)
    theme_list = Theme.objects.all()
    raw_dict = []
    for theme in theme_list:
        theme_str = theme.theme_str
        num = Motion.objects.filter(Q(theme_top = theme_str)|Q(theme_add = theme_str)).filter(meta__in = meta_list).count()
        each = {'str':theme_str,'num':num}
        raw_dict.append(each)

    context = {
        'dir' : Meta.possession(tournament),
        'dict' : refineDict(raw_dict),
        'style_str' : style_str,
        'level_str' : level_str,
        'msg_id' : request.GET.get("msg"),
        'ongoing' : tournament.ongoing,
    }

    return render(request, "tournaments/each.html", context)

def refineDict(dict):
    total = 0
    for each in dict:
        total += each["num"]
    
    other = 0
    dels = []
    for each in dict:
        if each["num"] / total < 0.03:
            other += each["num"]
            dels.append(each)
    
    for each in dels:
        dict.remove(each)
    
    others = {"str":"others","num":other}
    dict.append(others)
    
    return dict

def build(request):
    if request.method == "POST":
        name = request.POST.get("name")
        style = request.POST.get("s1")
        level = request.POST.get("s2")
        id = Tournament.objects.order_by('id').last().id + 1
        Tournament.objects.create(id=id,tournament_name=name,style=style,level=level)
        url = "/tournaments/?msg=1&id=" + str(id)
        return redirect(url)

    tournament_list = Tournament.objects.all()
    tournament_json = ",".join(list(map(lambda t : t.to_json(),tournament_list)))
    context = {
        'tournament_json' : tournament_json,
    }
    return render(request, "tournaments/build.html", context)
