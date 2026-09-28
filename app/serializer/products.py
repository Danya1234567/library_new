from rest_framework import serializers
from app.models import Categories, Suppliers, Products


class ProductsSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Categories.objects.all())
    supplier = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Suppliers.objects.all())
    class Meta:
        model = Products
        fields = '__all__'