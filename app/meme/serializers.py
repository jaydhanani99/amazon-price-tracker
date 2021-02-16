from rest_framework import serializers

from core.models import Meme


class MemeSerializer(serializers.ModelSerializer):
    """Serializer for Meme Objects"""

    class Meta:
        model = Meme
        fields = ('id', 'name', 'url', 'caption', 'created_at')
        read_only_fields = ('id', 'created_at')
    
class MemeSerializerWithoutName(serializers.ModelSerializer):
    """Serializer for Meme Objects without name field"""

    class Meta:
        model = Meme
        fields = ('id', 'name', 'url', 'caption', 'created_at')
        read_only_fields = ('id','name', 'created_at')

        

