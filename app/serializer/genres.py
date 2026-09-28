from rest_framework import serializers
from app.models import Genres


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model=Genres
        fields='__all__'