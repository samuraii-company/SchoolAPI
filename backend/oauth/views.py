from rest_framework import generics
from .models import User
from . import serializer


class RegisterView(generics.CreateAPIView):
    """Create account"""

    queryset = User.objects.all()
    serializer_class = serializer.RegisterSerializer