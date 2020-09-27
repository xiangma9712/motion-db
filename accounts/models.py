from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class Evaluator(models.Model):
    user = models.OneToOneField(User, related_name='eval', on_delete=models.CASCADE)
    evaluated_list = ArrayField(models.IntegerField())
    def __str__(self):
        return self.user.name
