from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    language = serializers.StringRelatedField(many=False, read_only=False)
    author = serializers.StringRelatedField(many=True, read_only=False)

    class Meta:
        model = Book
        fields = '__all__'
        depth = 0
