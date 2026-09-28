from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from users.models import User



class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'phone_number',
            'password',
            'email'
        ]

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)