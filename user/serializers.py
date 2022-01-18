from django.contrib.auth import get_user_model
from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):
    ''' serializamos el usuario normal '''
    def test_from_test(self):
        pass
    