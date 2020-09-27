from rest_framework import serializers
from home.models import Motion, Copy, AsianSet

class MotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motion
        fields = ('id', 'motion_text','info_text','style','theme_top','theme_add')
        
class CopySerializer(serializers.ModelSerializer):
    class Meta:
        model = Copy
        fields = ('motion_id',)

class AsianSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsianSet
        fields = ("id","one_id","two_id","three_id")
