from django.db import transaction
from rest_framework import serializers

from app.models import ChillZones, Orders, Payments, Receipts, ReceiptProducts, Products, PaymentTypes
from app.serializer.payment import PaymentsSerializer
from users.models import Employee
from users.serializer.user import UserSerializer


class EmployeeOrderSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    position = serializers.SlugRelatedField(slug_field='name_of_position', read_only=True)
    class Meta:
        model = Employee
        fields = ['id', 'name', 'phone_number', 'position']

class ChillZoneOrderSerializer(serializers.ModelSerializer):
    library = serializers.SlugRelatedField(slug_field='address', read_only=True)
    class Meta:
        model = ChillZones
        fields = ['id', 'branch', 'square', 'library']


class OrdersSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    employee = EmployeeOrderSerializer(read_only=True)
    payment = PaymentsSerializer(read_only=True)
    chill_zone = ChillZoneOrderSerializer(read_only=True)
    class Meta:
        model = Orders
        fields = '__all__'

class OrderProductInputSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all())
    quantity = serializers.IntegerField(min_value=1)


class OrdersWriteSerializer(serializers.ModelSerializer):
    products = OrderProductInputSerializer(many=True, write_only=True)
    payment_type = serializers.PrimaryKeyRelatedField(queryset=PaymentTypes.objects.all(), write_only=True)

    class Meta:
        model = Orders
        fields = ['id', 'note', 'client', 'chill_zone', 'employee', 'payment_type', 'products']
        extra_kwargs = {'employee': {'required': False, 'allow_null': True}, 'client': {'required': False}}

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        payment_type = validated_data.pop('payment_type')

        total_price = sum(item['product'].price * item['quantity'] for item in products_data)

        with transaction.atomic():
            payment = Payments.objects.create(price=total_price, is_success=True, payment_type=payment_type)
            order = Orders.objects.create(payment=payment, **validated_data)
            receipt = Receipts.objects.create(order=order)
            ReceiptProducts.objects.bulk_create([
                ReceiptProducts(
                    receipt=receipt,
                    product=item['product'],
                    quantity=item['quantity'],
                    total_amount=item['product'].price * item['quantity'],
                )
                for item in products_data
            ])

        return order