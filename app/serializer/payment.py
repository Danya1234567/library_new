from rest_framework import serializers

from app.models import PaymentTypes, Payments


class PaymentsSerializer(serializers.ModelSerializer):
    payment_type = serializers.SlugRelatedField(
        slug_field='name',
        queryset=PaymentTypes.objects.all(),
    )
    class Meta:
        model=Payments
        fields='__all__'