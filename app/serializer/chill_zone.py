from rest_framework import serializers
from app.models import CategoryChillZones, ChillZones, ChillZoneBookings
from app.serializer.category import CategorySerializer
from app.serializer.libraries import LibrariesSerializer


class CategoryChillZoneShortSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = CategoryChillZones
        fields = ['category', 'is_available']


class ChillZonesSerializer(serializers.ModelSerializer):
    library = LibrariesSerializer(read_only=True)
    categories = CategoryChillZoneShortSerializer(source='category_chill_zones', many=True, read_only=True)
    orders_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = ChillZones
        fields = '__all__'

class CategoryChillZonesSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    chill_zone = ChillZonesSerializer(read_only=True)
    class Meta:
        model = CategoryChillZones
        fields = '__all__'

class ChillZonesWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChillZones
        fields = ['id', 'name', 'branch', 'capacity', 'is_active', 'square', 'library', 'payment_type', 'free_seats']

    def validate(self, data):
        capacity = data.get('capacity', getattr(self.instance, 'capacity', None))
        free_seats = data.get('free_seats', getattr(self.instance, 'free_seats', None))
        if capacity is not None and free_seats is not None and free_seats > capacity:
            raise serializers.ValidationError('The number of available seats cannot exceed the total capacity.')
        return data

class ChillZoneBookingSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(slug_field='phone_number', read_only=True)
    chill_zone = ChillZonesSerializer(read_only=True)
    class Meta:
        model = ChillZoneBookings
        fields = ['id', 'client', 'chill_zone', 'seats', 'created_at', 'is_active']


class ChillZoneBookingWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChillZoneBookings
        fields = ['id', 'chill_zone', 'seats']
    def validate(self, data):
        chill_zone = data['chill_zone']
        seats = data['seats']
        if not chill_zone.is_active:
            raise serializers.ValidationError('This zone is currently unavailable.')
        if seats > chill_zone.free_seats:
            raise serializers.ValidationError('Not enough available spaces.')
        return data

class CategoryChillZonesWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryChillZones
        fields = ['id', 'category', 'chill_zone', 'is_available']