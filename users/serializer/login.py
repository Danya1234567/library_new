from django.contrib.auth import authenticate
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        user = authenticate(
            request=self.context.get('request'),
            username=data['username'],
            password=data['password'],)
        if not user:
            raise serializers.ValidationError('Invalid username or password. ＞﹏＜')
        if not user.is_active:
            raise serializers.ValidationError('The account is disabled.')
        if not user.is_email_verified:
            raise serializers.ValidationError('Please verify your email before logging in.')
        data['user'] = user
        return data
