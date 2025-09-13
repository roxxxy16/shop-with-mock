from django.contrib import admin
from django.urls import path, re_path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from users import views

schema_view = get_schema_view(
    openapi.Info(
        title="Shop API",
        default_version='v1',
        description="Документация для магазина",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/registration/', views.RegistrationView.as_view(), name="registration"),
    path("api/v1/user/login/", views.LoginView.as_view(), name="login"),
    path("api/v1/user/logout/", views.LogoutView.as_view(), name="logout"),
    path("api/v1/user/delete/", views.DeleteView.as_view(), name="delete"),
    path('api/v1/catalog/', views.CatalogView.as_view(), name="catalog"),
    path('api/v1/cart/', views.CartView.as_view(), name="cart"),
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
