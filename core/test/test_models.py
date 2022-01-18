from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    
    def test_create_user_with_email_successful(self):
        ''' probar crear usuario con email '''
        email = 'test@walii.es'
        password = 'test123'
        
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )
        
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    
    def test_new_user_normalized(self):
        ''' controla que el mail del usuario se ha normalizado '''
        email = 'test@WALII.ES'
        password = 'test123'
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )
        
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        ''' verificar que el email es correcto '''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
            email = None,
            password = 'pass'
        )
        
    def test_create_superuser(self):
        ''' probar super user '''
        email = 'test@walii.es'
        password = 'test123'
        user = get_user_model().objects.create_super_user(
            email = email,
            password = password
        )
        
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)