from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from base import mods
from django.urls import reverse

class AuthTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)
        u = User(username='voter1')
        u.set_password('123')
        u.save()

        u2 = User(username='admin')
        u2.set_password('admin')
        u2.is_superuser = True
        u2.save()

    def tearDown(self):
        self.client = None

    def test_login(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)

        token = response.json()
        self.assertTrue(token.get('token'))

    def test_login_fail(self):
        data = {'username': 'voter1', 'password': '321'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_getuser(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 200)

        user = response.json()
        self.assertEqual(user['id'], 1)
        self.assertEqual(user['username'], 'voter1')

    def test_getuser_invented_token(self):
        token = {'token': 'invented'}
        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 404)

    def test_getuser_invalid_token(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 1)

        token = response.json()
        self.assertTrue(token.get('token'))

        response = self.client.post('/authentication/logout/', token, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 404)

    def test_logout(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 1)

        token = response.json()
        self.assertTrue(token.get('token'))

        response = self.client.post('/authentication/logout/', token, format='json')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 0)

#Tests sin persistencia
class RegistrationTest(TestCase):

    def test_registration_view(self):
        # Prueba de registro exitoso
        response = self.client.post(reverse('register'), {'username': 'testuser23', 'password1': 'yhenenxmaawSNA@SMDNE', 'password2': 'yhenenxmaawSNA@SMDNE', 'email': 'testmail@gmail.com', 'firstname': 'testname', 'lastname':'testlastname'})
        self.assertEqual(User.objects.filter(username='testuser23').count(), 1)

    def test_registration_invalid_form(self):
        # Prueba de registro con formulario inválido
        response = self.client.post(reverse('register'), {'username': 'testuser'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

    def test_registration_password_mismatch(self):
        # Prueba de registro con contraseñas que no coinciden
        response = self.client.post(reverse('register'), {'username': 'testuser', 'password1': 'testpass', 'password2': 'wrongpass', 'email': 'testmail@gmail.com', 'firstname': 'testname', 'lastname':'testlastname'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The two password fields didn’t match.')
    def test_registration_existing_user(self):
        # Prueba de registro con un usuario que ya existe
        User.objects.create_user(username='existinguser', password='testpass')
        response = self.client.post(reverse('register'), {'username': 'existinguser', 'password1': 'testpass', 'password2': 'testpass'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A user with that username already exists.')

    def test_registration_blank_fields(self):
        # Intentar registrar un usuario con campos en blanco
        data = {
            'username': '',
            'password1': '',
            'password2': '',
            'email': '',
        }
        response = self.client.post(reverse('register'), data)
        self.assertContains(response, 'This field is required.')

    def test_registration_weak_password(self):
        # Intentar registrar un usuario con una contraseña débil
        data = {
            'username': 'weakuser',
            'password1': '123456',  # Contraseña débil
            'password2': '123456',
            'email': 'weakuser@example.com',
        }
        response = self.client.post(reverse('register'), data)
        self.assertContains(response, 'This password is too common.')
