from rest_framework import serializers
from app.models import PaymentTypes


class PaymentTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model=PaymentTypes
        fields='__all__'