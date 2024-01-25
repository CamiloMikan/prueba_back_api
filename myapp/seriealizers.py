from rest_framework import serializers
from .models import Clients, Bills, Products
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JwtTokenObtainPairSerializer
from django.contrib.auth.models import User
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bills
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'    
class ClientImportSerializer(serializers.Serializer):
    file = serializers.FileField()
    
  

    
class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    username_field = 'email' 

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password')
        
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(email=validated_data['email'], username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user