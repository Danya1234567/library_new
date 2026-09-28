from rest_framework import serializers
from app.models import Positions


class PositionSerializer(serializers.ModelSerializer):
    default_group_name = serializers.CharField(source='default_group.name', read_only=True)
    class Meta:
        model=Positions
        fields=['id', 'name_of_position', 'default_group', 'default_group_name']