from rest_framework import serializers
from app.models import Genres, Books


class BooksSerializer(serializers.ModelSerializer):
    author_ids = serializers.PrimaryKeyRelatedField(source='author', many=True, read_only=True)
    genre_ids = serializers.PrimaryKeyRelatedField(source='genre', many=True, read_only=True)
    total_borrows = serializers.IntegerField(read_only=True)
    currently_borrowed = serializers.IntegerField(read_only=True)
    author = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        read_only=True,)
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=
        Genres.objects.all(),)
    class Meta:
        model=Books
        fields='__all__'

class BooksWriteSerializer(serializers.ModelSerializer):
    rented = serializers.IntegerField(read_only=True)

    class Meta:
        model = Books
        fields = [
            'id', 'name', 'release_date', 'original_language',
            'rented', 'price', 'rent_price', 'is_allowed', 'image_url', 'author', 'genre',
        ]