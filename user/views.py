from django.shortcuts import render

# Create your views here.
from user.serializers import UserSerializer, AuthTokenSerializer

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateUserView(generics.CreateAPIView):
    ''' create user '''
    serializer_class = UserSerializer
    
class CreateTokenView(ObtainAuthToken):
    ''' creamos un token para usuario '''
    serializer_class = UserSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    ''' manejar usuario authenticado '''
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, )
    
    def get_object(self):
        return self.request.user