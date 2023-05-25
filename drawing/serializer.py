from rest_framework import serializers

from drawing.models import Animation, Drawing


class DrawingPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drawing
        fields = ['name', "file", "user"]


class DrawingInfoSerializer(serializers.ModelSerializer):
    link = serializers.ReadOnlyField(source='file.url')

    class Meta:
        model = Drawing
        fields = ['id', "name", "link", "status"]


class AnimationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animation
        fields = ['id', "drawing_id", "link", "purpose"]


class AnimationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animation
        fields = ['id', "drawing_id", "link", "purpose"]
