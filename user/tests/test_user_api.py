from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient




CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')



def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)

class PublicUserApiTests(TestCase):
    ''' test api publica de usuarios '''
    
    def setUp(self):
        self.client = APIClient()
        
    def test_create_valid_user_success(self):
        payload = {
            'email': 'test@walii.es',
            'password': 'password',
            'name': 'test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        # verifica que se crea la pagina de usuario
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        # verifica que la password es correcta
        self.assertTrue(user.check_password(payload['password']))
        # verifica que la password no esta en los data
        self.assertNotIn('password', res.data)
        
    def test_user_exists(self):
        payload = {
            'email':'test@walii.es',
            'password': 'password',
            'name': 'test name'
        }
        create_user(**payload)
        
        res = self.client.post(CREATE_USER_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_password_too_short(self):
        payload = {
            'email':'test@walii.es',
            'password': 'po',
            'name': 'test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        # verificamos si la clave es muy corta
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        # verificamos si el usuario ya existe
        user_exists = get_user_model().objects.filter(email=payload['email'])
        self.assertFalse(user_exists)
        
    # def test_create_token_for_user(self):
    #     ''' verificamos que hemos creado un token'''
        
    #     payload = {
    #         'email': 'test2222@walii.es',
    #         'password': 'po',
    #         'name': 'test 21312 name'
    #     }
    #     create_user(**payload)
    #     res = self.client.post(TOKEN_URL, payload)
        
    #     self.assertIn('token', res.data)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_create_token_invalid_creadentials(self):
        ''' probar que no se crea token con las credenciales invalidas '''

        create_user(email='test@walii.es', password='po')
        payload = {
            'email':'test@walii.es',
            'password': 'wrong',
        }
        res = self.client.post(TOKEN_URL, payload)
        
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_not_user(self):
        ''' no se crea token si no hay user name'''
        payload = {
            'email':'test@walii.es',
            'password': 'wrong',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_missing_field(self):
        ''' no se crea token si no hay user name, email or password'''
        payload = {
            'email':'one',
            'password': '',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorize(self):
        ''' prueba que esta autenticado el usuario '''

        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTests(TestCase):
    ''' test api privado de usuarios '''

    def setUp(self):
        self.user = create_user(
            email = 'test@walii.es',
            password = 'testpass',
            name = 'name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        ''' recuperar el perfil en caso de crear '''
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        ''' prueba que no se pueda hacer POST '''
        res = self.client.get(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        ''' probar que el usuario esta authenticado '''
        payload = {
            'password': 'newpassword',
            'name': 'test2 name'
        }
        res = self.client.patch(ME_URL, payload) 
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)