from rest_framework import serializers
from app.models import Shifts, Cities, PaymentTypes, Libraries, Books, LibraryBook


class LibrariesSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        read_only=True)
    shift = serializers.SlugRelatedField(
        many=True,
        slug_field='name_of_shift',
        queryset=Shifts.objects.all())
    city = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Cities.objects.all(),
    )
    payment_type = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=PaymentTypes.objects.all()
    )
    class Meta:
        model = Libraries
        fields = '__all__'

class LibraryBookSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(slug_field='name', read_only=True)
    library = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = LibraryBook
        fields = ['id', 'library', 'book', 'quantity']


class LibraryBookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryBook
        fields = ['id', 'library', 'book', 'quantity']

    def validate(self, data):
        if LibraryBook.objects.filter(library=data['library'], book=data['book']).exists():
            raise serializers.ValidationError('This book is already listed in this library—use the balance top-up option.')
        return data


class StockAdjustSerializer(serializers.Serializer):
    delta = serializers.IntegerField(help_text='Positive — deposit; negative — withdrawal.')