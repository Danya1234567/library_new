from rest_framework import serializers
from app.models import Shifts


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model=Shifts
        fields='__all__'