from rest_framework import serializers

from drawing.models import Animation, Drawing


class DrawingPostSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id')

    class Meta:
        model = Drawing
        fields = ['name', "file", "user_id"]


class DrawingInfoSerializer(serializers.ModelSerializer):
    link = serializers.ReadOnlyField(source='file.url')

    class Meta:
        model = Drawing
        fields = ['id', "name", "link", "status"]


class AnimationPostSerializer(serializers.ModelSerializer):
    drawing_id = serializers.IntegerField(source='drawing.id')

    class Meta:
        model = Animation
        fields = ["drawing_id", "file", "purpose"]


class AnimationInfoSerializer(serializers.ModelSerializer):
    link = serializers.ReadOnlyField(source='file.url')

    class Meta:
        model = Animation
        fields = ['id', "drawing_id", "link", "purpose"]
