from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .utils import MyTokenObtainPairView
from .views import RegisterView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
