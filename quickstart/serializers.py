from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from .models import Book, BookIssue
# from django.contrib.auth.hashers import make_password




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

''' extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data.pop('username', None) # remove username from validated_data
        email = validated_data['email']
        password = validated_data['password']
        user = User.objects.create(
            email=email,
            password=make_password(password),
        )
        if username:
            user.username = username
            user.save()
        return user'''

    

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BookIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookIssue
        fields = ['user', 'book', 'stat', 'issue_date', 'return_date']


