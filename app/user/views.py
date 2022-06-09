from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, TokenSerializer


class CreateUserView(generics.CreateAPIView):
    # Create a new user on the browser
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    # Create a new auth token for user
    serializer_class = TokenSerializer
    # Define a renderer function for viewing what happened in tha backend through the browser
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    # Manage the authenticated users
    serializer_class = UserSerializer

    authentication_classes = [authentication.TokenAuthentication]
    # To check if the user gets authentication to do some changes to the database
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Retrieve and return the authenticated user
        return self.request.user