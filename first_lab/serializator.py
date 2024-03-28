from django.contrib.auth.models import User
from rest_framework import serializers
from first_lab.models import *


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class BookLoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookLover
        fields = '__all__'
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'middle_name': {'required': False},
            'birthday': {'required': False},
            'date_of_joining': {'required': False},
            'address': {'required': False},
            'phone': {'required': False},
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # Создаем пользователя с помощью метода create_user
        return user


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'region']


class VolumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volume
        fields = ['id_volume', 'volume_number', 'number_of_pages']


class BookSerializer(serializers.ModelSerializer):
    volumes = VolumeSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id_book', 'title', 'publisher', 'year_of_release', 'cover_photo', 'volumes']

    def create(self, validated_data):
        volumes_data = validated_data.pop('volumes', [])
        book = Book.objects.create(**validated_data)
        for volume_data in volumes_data:
            Volume.objects.create(book=book, **volume_data)
        return book
