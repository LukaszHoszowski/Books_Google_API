from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    language = serializers.StringRelatedField(many=False, read_only=True)
    # author = serializers.ManyRelatedField(many=True, read_only=True)

    class Meta:
        model = Book
        fields = '__all__'
        depth = 1
