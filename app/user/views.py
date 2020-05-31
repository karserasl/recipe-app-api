from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken  # Gonna extent it
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Creating a new auth token for user"""
    serializer_class = AuthTokenSerializer

    # Sets the renderer so we can view the endpoint in the browser.
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
