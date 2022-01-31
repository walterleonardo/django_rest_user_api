from wsgiref import validate
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import gettext as _



class UserSerializer(serializers.ModelSerializer):
    ''' serializamos el usuario normal '''
    
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5 }}
        
    def create(self, validated_data):
        ''' creamos un nuevo usuario '''
        return get_user_model().objects.create_user(**validated_data)


    def update(self, instance, validated_data):
        ''' actualiza usuario'''
        password = validated_data.pop('password')
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        
        return user
    
class AuthTokenSerializer(serializers.Serializer):
    ''' serializador para el token '''
    email = serializers.CharField()
    password = serializers.CharField(
        style = {'input_type': 'password'},
        trim_whitespace=False
    )
    
    def validate(self, *args, **kwargs):
        ''' validador de usuario '''
        email = kwargs.get('email')
        password = kwargs.get('password')
        
        user = authenticate(
            request = self.context.get('request'),
            username = email,
            password = password
        )
        if not user:
            msq = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')
        
        kwargs['user'] = user
        return kwargs
        