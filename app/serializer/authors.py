from rest_framework import serializers
from app.models import Authors


class AuthorsSerializer(serializers.ModelSerializer):
    total_borrows = serializers.IntegerField(read_only=True)
    currently_borrowed = serializers.IntegerField(read_only=True)
    class Meta:
        model = Authors
        fields = '__all__'