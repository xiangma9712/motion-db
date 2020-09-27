from django.contrib import admin
from .models import *

class SettingAdmin(admin.ModelAdmin):
    fieldsets = [ 
        ('Meta',   {'fields': ['name','info']}),
        ('Detail', {'fields': ['int','str']}),
    ]
    list_display = ['name','info','int','str']
    readonly_fields = ['name']

admin.site.register(Motion)
admin.site.register(Meta)
admin.site.register(Tournament)
admin.site.register(Round)
admin.site.register(Theme)
admin.site.register(Setting, SettingAdmin)
admin.site.register(Message)
admin.site.register(Copy)
admin.site.register(AsianSet)