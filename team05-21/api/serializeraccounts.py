from rest_framework import serializers
from Accounts import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.MyUser
