from django.urls import path
from .views import UserLoginView, UserRegisterView

urlpatterns = [
    path('signin', UserLoginView.as_view(), name="signin-page"),
    path('signup', UserRegisterView.as_view(), name="signup-page"),
    # path('token/veify', TokenVerifyView.as_view(), name="user-token-verify"),
    # path('refresh/token/', RefreshTokenView.as_view(), name="refresh-token-verify")
]