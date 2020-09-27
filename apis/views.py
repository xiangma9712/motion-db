import django_filters
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
from django.utils import timezone
from home.models import Motion, Copy, AsianSet
from .serializer import *


class MotionViewSet(viewsets.ModelViewSet):
    queryset = Motion.objects.all()
    serializer_class = MotionSerializer

    @action(detail=False)
    def clear(self,request):
        target = Motion.objects.filter(info_text=None)
        for mo in target:
            mo.info_text = ""
            mo.save()
        return Response({'status' : 'cleaned'})

class AsianSetViewSet(viewsets.ModelViewSet):
    queryset = AsianSet.objects.all()
    serializer_class = AsianSetSerializer
    
    @action(detail=False)
    def theme(self,request):
        sets = AsianSet.objects.all()
        for each in sets:
            each.update_theme()
        return Response({'status' : 'updated'})

class CopyViewSet(viewsets.ModelViewSet):
    queryset = Copy.objects.all()
    serializer_class = CopySerializer

    def create(self,request):
        id = request.data.get('motion_id')        
        Copy.objects.create(motion_id=id, date=timezone.localtime())
        return Response({'status' : 'recorded'})

    @action(detail=False)
    def clear(self,request):
        records = Copy.objects.all()
        motions = Motion.objects.all()
        
        dir = {}
        for copy in records:
            if not copy.is_new():
                copy.delete()
            else:
                key = str(copy.motion_id)
                if key in dir:
                    dir[key] += 1
                else:
                    d_each = {key : 1}
                    dir.update(d_each)
        
        targets = []
        for id_str in dir:
            targets.append(int(id_str))
        
        for motion in motions:
            if motion.id in targets:
                motion.copy_num = dir[str(motion.id)]
            else:
                motion.copy_num = 0
        
        Motion.objects.bulk_update(motions, ['copy_num'])
        
        return Response({'status' : 'cleaned'})
