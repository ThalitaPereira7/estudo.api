from rest_framework import serializers
from .models import Book
from .models import CustomUser



class BookSerializer(serializers.ModelSerializer):
 class Meta:
    model = Book
    fields = '__all__'
 
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number', 'is_premium']
        
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
