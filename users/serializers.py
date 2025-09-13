from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "second_name"]


class RegistrationsSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=128, min_length=1)
    second_name = serializers.CharField(max_length=128, min_length=1)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)
    
    def validate(self, attrs):
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError("Такой email уже зарегистрирован.")
        
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Пароли не совпадают.")
        
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        
        user = User.objects.create_user(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            second_name=validated_data["second_name"],
            password=validated_data["password"]
        )
        return user
    

class UpdateProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=128, min_length=1)
    second_name = serializers.CharField(max_length=128, min_length=1)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name),
        instance.second_name = validated_data.get("second_name", instance.second_name)
        instance.save()
        return instance
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Аккаунта с указанным email не существует.")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Не верный пароль.")
        
        if not user.is_active:
            raise serializers.ValidationError("Пользователь деактивирован.")
        
        data = super().validate(attrs)
        refresh = self.get_token(user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user"] = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "second_name": user.second_name,
        }
        return data