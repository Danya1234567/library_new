from rest_framework import serializers

from app.models import Receipts, Suppliers, Products, ReceiptProducts
from app.serializer.category import CategorySerializer
from app.serializer.order import OrdersSerializer


class ReceiptsSerializer(serializers.ModelSerializer):
    order = OrdersSerializer(read_only=True)
    class Meta:
        model=Receipts
        fields='__all__'

class SupplierShortSerializer(serializers.ModelSerializer):
    class Meta:
        model=Suppliers
        fields=['name','phone_number','email']

class ProductShortSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    supplier = SupplierShortSerializer(many=True)
    class Meta:
        model=Products
        fields=['name','price','date_of_expiry','category','supplier']

class ReceiptProductsSerializer(serializers.ModelSerializer):
    receipt=ReceiptsSerializer(read_only=True)
    product=ProductShortSerializer(read_only=True)
    class Meta:
        model=ReceiptProducts
        fields='__all__'