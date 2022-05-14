from rest_framework import serializers
from Profile import models


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.School


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Course


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Module


class CourseModulesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.CourseModules


class UserModulesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.UserModules


class LikedVideosSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.LikedVideos


class DislikedVideosSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.DislikedVideos


class ReportedVideosSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.ReportedVideos


class SavedVideosSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.SavedVideos


class LikedCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.LikedComments


class DislikedCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.DislikedComments


class ReportedCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.ReportedComments
