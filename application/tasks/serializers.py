from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class TaskSerializer(serializers.ModelSerializer):
    przypisany_uzytkownik = UserSerializer(read_only=True)
    przypisany_uzytkownik_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='przypisany_uzytkownik',
        write_only=True,
        required=False
    )

    autor = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'nazwa',
            'opis',
            'status',
            'przypisany_uzytkownik',
            'przypisany_uzytkownik_id',
            'autor',
        ]

