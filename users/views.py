from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.permissions import HasModulePermission

from .serializers import CustomTokenObtainPairSerializer, RegistrationsSerializer, UpdateProfileSerializer, UserInfoSerializer


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationsSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_serializer = UserInfoSerializer(user)

            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            return Response(
                {
                    "message": "Вы успешно зарегистрированны.",
                    "user": response_serializer.data,
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(access),
                    }
                },
                status=status.HTTP_201_CREATED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UpdateProfileView(APIView):
    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = UpdateProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            updated_user = serializer.save()
            response_serializer = UserInfoSerializer(updated_user)
            return Response(
                {
                    "message": "Вы успешно изменили данные.",
                    "user": response_serializer.data
                },
                status=status.HTTP_200_OK
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"detail": "Нужен refresh token."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(
                {"detail": "Неверный refresh token."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": "Вы успешно вышли из аккаунта."},
            status=status.HTTP_200_OK
        )


class DeleteView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        user.is_active = False
        user.save()

        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            pass

        return Response({"message": "Вы успешно деактивировали свой аккаунт."},status=status.HTTP_202_ACCEPTED)
    

class CatalogView(APIView):
    permission_classes = [HasModulePermission]
    module = "Catalog"

    def get(self, request):
        return Response(
            {
                "items": [
                    {"id": 1, "name": "Товар 1"},
                    {"id": 2, "name": "Товар 2"},
                ]
            },
            status=status.HTTP_200_OK
        )
    
    def post(self, request, *args, **kwargs):
        return Response(
            {
                "message": "Вы успешно добавили новый товар.",
                "items": [
                    {"id": 1, "name": "Товар 1"},
                ]
            },
            status=status.HTTP_201_CREATED
        )
    
    def patch(self, request, *args, **kwargs):
        return Response(
            {
                "message": "Вы успешно изменили товар.",
                "items": [
                    {"id": 1, "name": "Товар 1"},
                ]
            },
            status=status.HTTP_200_OK
        )
    
    def delete(self, request, *args, **kwargs):
        return Response(
            {
                "message": "Вы успешно удалили товар.",
                "items": [
                    {"id": 1, "name": "Товар 1"},
                    {"id": 2, "name": "Товар 2"},
                ]
            },
            status=status.HTTP_200_OK
        )


class CartView(APIView):
    permission_classes = [HasModulePermission]
    module = "Cart"

    def get(self, request):
        return Response(
            {
                "items": [
                    {"id": 1, "name": "Товар 1", "quantity": 1},
                    {"id": 2, "name": "Товар 2", "quantity": 2},
                ]
            },
            status=status.HTTP_200_OK
        )
    
    def post(self, request, *args, **kwargs):
        return Response(
            {
                "message": "Вы успешно добавили новый товар в корзину.",
                "items": [
                    {"id": 1, "name": "Товар 1", "quantity": 1},
                ]
            },
            status=status.HTTP_201_CREATED
        )
    
    def patch(self, request, *args, **kwargs):
        return Response(
            {
                "message": "Вы успешно изменили кол-во товаров в корзине.",
                "items": [
                    {"id": 1, "name": "Товар 1", "quantity": 5},
                ]
            },
            status=status.HTTP_200_OK
        )
    
    def delete(self, request, *args, **kwargs):
        return Response(
            {
                "message": "Вы успешно удалили товар из корзины.",
                "items": [
                    {"id": 2, "name": "Товар 2", "quantity": 3},
                ]
            },
            status=status.HTTP_200_OK
        )
