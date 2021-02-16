from rest_framework import serializers

from core.models import Product

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product Objects"""

    class Meta:
        model = Product
        fields = ('id', 'name', 'url', 'price', 'is_active', 'email')
        read_only_fields = ('id',)