from rest_framework import serializers

from drawing.models import Animation, Drawing


class DrawingPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drawing
        fields = ['name', "link", ]


class DrawingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drawing
        fields = ['id', "password", "email", ]


class AnimationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animation
        fields = ['id', "drawing_id", "link", "purpose"]


class AnimationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animation
        fields = ['id', "drawing_id", "link", "purpose"]
