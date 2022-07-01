from rest_framework import serializers

# models
from .models import Books

class BooksSerializer(serializers.ModelSerializer):
    books_register = serializers.ReadOnlyField(source='books_register.username')
    
    class Meta:
        model = Books
        fields = ('id', 'title', "subtitle", "books_author", "books_category", "published_date", "book_editor", "description", "picture", "books_register", "created", "modified")
