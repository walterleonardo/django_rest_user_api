from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient




CREATE_USER_URL = reverse('user:create')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)

class PublicUserApiTests(TestCase):
    ''' test api publica de usuarios '''
    
    def setUp(self):
        self.client = APIClient()
        
    def test_create_valid_user_success(self):
        payload = {
            'email':'test@walii.es',
            'password': 'password',
            'name': 'test name'
        }
        
        res = self.client.post(CREATE_USER_URL, payload=payload)
        # verifica que se crea la pagina de usuario
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user =get_user_model().objects.get(**res.data)
        # verifica que la password es correcta
        self.assertTrue(user.check_password(payload['password']))
        # verifica que la password no esta en los data
        self.assertNotIn('password', res.data)
        
    def test_user_exists(self):
        payload = {
            'email':'test@walii.es',
            'password': 'password',
        }
        create_user(**payload)
        
        res = self.client.post(CREATE_USER_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_password_too_short(self):
        payload = {
            'email':'test@walii.es',
            'password': 'po',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        # verificamos si la clave es muy corta
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        # verificamos si el usuario ya existe
        user_exists = get_user_model().objects.filter(email=payload['email'])
        self.assertFalse(user_exists)