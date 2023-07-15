
from rest_framework import serializers
from django.contrib.auth import get_user_model
Client = get_user_model()
from django.contrib.auth.hashers import make_password

from .models import SubscriptionPlans, Chat
from client.models import ClientAdditionalDetails

from client.models import Subscriptions



class AdminUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'is_staff','is_active','image')

    def create(self, validated_data):
        image = validated_data.get('image', None)
        if image:
            user = Client.objects.create(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                email=validated_data['email'],
                password=make_password(validated_data['password']),
                image=image,
            )
        else:
            user = Client.objects.create(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                email=validated_data['email'],
                password=make_password(validated_data['password']),
            )
        
        return user


class SubsriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlans
        fields = '__all__'


class CreateSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = ('subscription_plan', 'client', 'payment_id') 



class CreateClientAdditionalDetails(serializers.ModelSerializer):
    class Meta:
        model = ClientAdditionalDetails
        fields = ('__all__') 

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'




