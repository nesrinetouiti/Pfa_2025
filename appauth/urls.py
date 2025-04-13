from django.urls import path
from .views import register_user, login_user, CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView,
)

urlpatterns = [
    path('register/', register_user, name='register_user'),
    # If you still want to keep your simple custom login, you can include it:
    path('custom-login/', login_user, name='login_user'),

    # Use the custom JWT login view with extra user info:
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # The remaining JWT endpoints:
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
