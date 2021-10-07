
from rest_framework import serializers
from .models import User,UserProfile,Product
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings




class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('name', 'phone')


class UserRegistrationSerializer(serializers.ModelSerializer):

    profile = UserSerializer(required=False)

    class Meta:
        model = User
        fields = ('username','email', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(
            user=user,
            name=profile_data['name'],
            phone=profile_data['phone'],
           
        )
        return user




JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given username and password does not exists'
            )
        return {
            'username':user.username,
            'token': jwt_token
        }


###################### Product Serilizer ####################



class ProductlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('sku','name', 'description','category','price','metadata')
        

    def create(self, validated_data):
        productlist = Product.objects.create(**validated_data)
        
        return productlist
    
    def delete(self, validated_data):
        productlist = Product.objects.get(**validated_data)
        productlist.delete()
        return productlist


