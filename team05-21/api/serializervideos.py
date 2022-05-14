from rest_framework import serializers
from Videos import models


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Video


class VideoModulesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.VideoModules


class VideoNoteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.VideoNote


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Comment
