
from django.contrib.auth.models import User
from django.db.models import fields
from django.utils.translation import activate
from rest_framework import serializers
from .mail import *
import uuid
from .models import *
import random
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required = True)
    class Meta:
        model = User
        fields = ['username' , 'email' , 'password' , 'first_name' , 'last_name']

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        first_name = None
        last_name = None

        if 'first_name' in validated_data:
            first_name = validated_data['first_name']
        
        if 'last_name' in validated_data:
            last_name = validated_data['last_name']

        obj = User.objects.create(
            username = username,
            email = email,
            first_name = first_name,
            last_name = last_name)

        obj.set_password(password)
        obj.save()
        token =random.randint(10000 , 99999)
        activate_url = f'{token}'
        Profile.objects.create(
            user = obj,
            token = token
        )
        send_activation_email(obj.email , 
                            obj.first_name,activate_url)
        
        return obj




# class RegisterSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     email = serializers.EmailField()
#     password = serializers.CharField()
#     first_name = serializers.CharField()
#     last_name = serializers.CharField()

