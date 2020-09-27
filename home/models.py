from django.db import models
from django.utils import timezone
import datetime
from django.contrib.postgres.fields import ArrayField

class Tournament(models.Model):
    BP    = 0
    ASIAN = 1
    NA    = 2

    ROOKIE        = 0
    DOMESTIC      = 1
    INTERNATIONEL = 2
    PRO_AM        = 3

    tournament_name = models.CharField(max_length=30)
    style = models.IntegerField()
    level = models.IntegerField()
    ongoing = models.BooleanField(default = True)
    def __str__(self):
        return self.tournament_name
    def to_json(self):
        return '["' + self.tournament_name + '",' + str(self.style) + ',' + str(self.level) + ',' + str(self.id) +']'

class Meta(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    year       = models.IntegerField()
    round      = models.CharField(max_length=10)
    style      = models.IntegerField(null=True)
    def __str__(self):
        data = str(self.tournament) + '",' + str(self.year) + ',"' + self.round
        return '"' + data + '"'
    def to_json(self):
        return '[' + ','.join([str(self.id),str(self.year)]) + ',"' + self.round + '"' + ',' + str(self.tournament_id) + ']'

    @staticmethod
    def possession(tournament):
        meta_list = Meta.objects.filter(tournament=tournament)
        num = len(meta_list)
        if tournament.style == 1:
            num *= 3
        try:
            min = meta_list[0].year
            max = meta_list[0].year
            for meta in meta_list:
                if meta.year > max:
                    max = meta.year
                elif meta.year < min:
                    min = meta.year
        except:
            min = "n/a"
            max = "n/a"

        dir = {
            'num' : num,
            'min' : min,
            'max' : max,
            'name': tournament.tournament_name,
            'id'  : tournament.id,
        }
        return dir
class Round(models.Model):
    round_str = models.CharField(max_length = 10)
    is_preliminary = models.BooleanField(default=False,null=True)
    def __str__(self):
        return self.round_str
    def to_json(self):
        return '[' + str(self.id) + ',"' + self.round_str + '","' + str(self.is_preliminary) + '"]'

class Motion(models.Model):
    motion_text = models.CharField(max_length=1000, blank=True, null=True)
    info_text   = models.CharField(max_length=1500, blank=True, null=False, default="")
    theme_top   = models.CharField(max_length=25, blank=True, null=False, default="")
    theme_add   = models.CharField(max_length=25, blank=True, null=False, default="")
    tournament  = models.ForeignKey(Tournament, on_delete=models.CASCADE,null=True)
    round       = models.ForeignKey(Round, on_delete=models.CASCADE,null=True)
    year        = models.IntegerField(default=0)
    meta        = models.ForeignKey(Meta, on_delete=models.CASCADE,null=True)
    style       = models.IntegerField(null=True)
    copy_num    = models.IntegerField(default=0)
    easy_opp    = ArrayField(models.IntegerField(), default=list)
    leaning_opp = ArrayField(models.IntegerField(), default=list)
    fair        = ArrayField(models.IntegerField(), default=list)
    leaning_gov = ArrayField(models.IntegerField(), default=list)
    easy_gov    = ArrayField(models.IntegerField(), default=list)
    fairness    = models.FloatField(default=2)
    def __str__(self):
        return self.motion_text
    def to_json(self):
        return '[' + ','.join([str(self.id),self.round,]) + ']'
    def to_json_2(self):
        return '[' + str(self.meta_id) + ',' + str(self.id) + ']'
    def calc_fairness(self):
        eg = len(self.easy_gov)
        eo = len(self.easy_opp)
        lg = len(self.leaning_gov)
        lo = len(self.leaning_opp)
        fa = len(self.fair)
        total = eg + eo + lg + lo + fa
        if total < 1:
            self.fairness = 2
            self.save()
            return
        ratio = 1 - fa / total
        mean = (eg - eo + 0.5 * lg - 0.5 * lo) / total
        self.fairness = ratio * mean * mean
        self.save()

    def record_evaluation(self,score,user_id):
        if score == 1:
            self.easy_gov.append(user_id)
        elif score == 0.5:
            self.leaning_gov.append(user_id)
        elif score == 0:
            self.fair.append(user_id)
        elif score == -0.5:
            self.leaning_opp.append(user_id)
        else:
            self.easy_opp.append(user_id)
        self.calc_fairness()
        self.save()
    def change_evaluation(self,score,user_id):
        if user_id in self.easy_gov:
            self.easy_gov.remove(user_id)
        elif user_id in self.leaning_gov:
            self.leaning_gov.remove(user_id)
        elif user_id in self.fair:
            self.fair.remove(user_id)
        elif user_id in self.easy_opp:
            self.easy_opp.remove(user_id)
        elif user_id in self.leaning_opp:
            self.leaning_opp.remove(user_id)
        self.save()
        self.record_evaluation(score,user_id)

    def past_evaluation(self,user_id):
        if user_id in self.easy_gov:
            return 1
        elif user_id in self.leaning_gov:
            return 0.5
        elif user_id in self.fair:
            return 0
        elif user_id in self.easy_opp:
            return -1
        elif user_id in self.leaning_opp:
            return -0.5
        else:
            return 2

    @staticmethod
    def possession(tournament):
        motion_list = Motion.objects.filter(tournament=tournament)
        num = len(motion_list)
        try:
            min = motion_list[0].year
            max = motion_list[0].year
            for motion in motion_list:
                if motion.year > max:
                    max = motion.year
                elif motion.year < min:
                    min = motion.year
        except:
            min = "n/a"
            max = "n/a"

        dir = {
            'num' : num,
            'min' : min,
            'max' : max,
            'name': tournament.tournament_name,
            'id'  : tournament.id,
        }
        return dir

class AsianSet(models.Model):
    one = models.ForeignKey(Motion, on_delete=models.CASCADE,related_name="one")
    two = models.ForeignKey(Motion, on_delete=models.CASCADE,related_name="two")
    three = models.ForeignKey(Motion, on_delete=models.CASCADE,related_name="three")
    theme = models.CharField(max_length=25, blank=True, null=False, default="")
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    year       = models.IntegerField()
    round      = models.ForeignKey(Round, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.tournament) + ',' + str(self.year) + ',' + str(self.round)
    def to_json(self):
        return '["' + str(self.id) + '","' + str(round) + '"]'
    def get_motion_ids(self):
        ids = [self.one.id,self.two.id,self.three.id]
        return ids
    def update_theme(self):
        themes = [
            self.one.theme_top,
            self.one.theme_add,
            self.two.theme_top,
            self.two.theme_add,
            self.three.theme_top,
            self.three.theme_add
        ]
        if len(themes) - len(set(themes)) < 2:
            return

        dup = list(set(themes))
        for each in dup:
            themes.remove(each)

        self.theme = themes[0]
        self.save()

class Theme(models.Model):
    theme_str = models.CharField(max_length = 25)
    deprecated = models.BooleanField(default=False,null=True)
    def __str__(self):
        return self.theme_str
    def to_json(self):
        return '[' + str(self.id) + ',"' + self.theme_str + '"]'

class Setting(models.Model):
    name = models.CharField(max_length = 15)
    info = models.CharField(max_length = 200, default='',null=True, blank=True)
    int  = models.IntegerField(null=True)
    str  = models.CharField(max_length = 15, default='',null=True, blank=True)
    def __str__(self):
        return self.name

class Message(models.Model):
    title = models.CharField(max_length = 30)
    body  = models.CharField(max_length = 3000)
    link_txt = models.CharField(max_length = 30,null=True, blank=True)
    url =  models.CharField(max_length = 200,null=True, blank=True)
    def __str__(self):
        return self.title

class Copy(models.Model):
    motion_id = models.IntegerField(default=0)
    date   = models.DateTimeField(default=timezone.datetime.today())
    def __str__(self):
        return str(self.date)
    def is_new(self):
        return self.date >= timezone.localtime() - datetime.timedelta(days=60)
