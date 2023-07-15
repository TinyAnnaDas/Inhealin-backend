from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Client, MoodJournal, TherapySessions

class TherapySessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TherapySessions
        fields = '__all__'

class CreateClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ("id", "name", "email", "phone", "password", "is_staff", "is_active", 'image')

    def create(self, validated_data):
        client = Client.objects.create_user(
            name = validated_data["name"],
            email = validated_data["email"],
            phone = validated_data["phone"],
            password = validated_data["password"],
        )
        return client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ("id", "name", "email", "phone", "is_active", "image")

from django.conf import settings
class MoodJournalSerializer(serializers.ModelSerializer):

    updated_at = serializers.DateTimeField(format=settings.DATETIME_FORMAT, input_formats=None)

    class Meta:
        model = MoodJournal
        fields = ("id", "journal", "client", "updated_at")



