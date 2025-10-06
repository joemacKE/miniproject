from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate



#registration serializer
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = [
                    'email',
                    'username',
                    'first_name',
                    'last_name',
                    'role',
                    'phone_number',
                    'password',
                    'confirm_password'
        ]

        def validate(self, data):
            if data['password'] != data['confirm_password']:
                raise serializers.ValidationError("Passwords do not match")
            return data
        
        def create(self, validated_data):
            password = validated_data.pop('password')
            confirm_password = validated_data.pop('confirm_password')

            user = User.objects.create_user(
                email = validated_data.get['email'],
                username = validated_data.get['username'],
                first_name = validated_data.get['first_name'],
                last_name = validated_data.get['last_name'],
                role = validated_data.get['role'],
                phone_number = validated_data.get['phone_number'],
            )
            user.save()
            return user
        
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        
        if not user.is_active:
            raise serializers.ValidationError("Account not active yet")
        
        data['user'] = user
        return data

class RoleTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super.get_token(user)
        token['role'] = user.role
        token['email'] = user.email
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)

        data.update({
            'user':{
                'id':self.user.id,
                'email':self.user.email,
                'role':self.user.role,
            }
        })
        return data

#user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

        

