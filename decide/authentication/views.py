from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED,
        HTTP_200_OK,
        HTTP_400_BAD_REQUEST,
        HTTP_401_UNAUTHORIZED,
        HTTP_404_NOT_FOUND
)
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from .serializers import UserSerializer


class GetUserView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        return Response(UserSerializer(tk.user, many=False).data)

class LogoutView(APIView):
    def post(self, request):
        try:
            key = request.data.get('token', '')
            Token.objects.filter(key=key).delete()
            return Response('User logout succesfully', status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response('', status=HTTP_404_NOT_FOUND)


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        )
        labels = {
            'username':('Username'),
            'first_name':('First Name'),
            'last_name':('Last Name'),
            'email':('Email'),
            'password':('Password')
        }
        #Revisar nombre de usuario(repeticiones, tamaño etc...), mirar formato y tamaño de email y comprobar tamaño de los campos de nombre y apellido.

class RegisterView(CreateView):
    
    def post(self, request):
        form = RegisterForm(request.data)
        if form.is_valid():
            user = form.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'user_pk': user.pk, 'token': token.key}, status=HTTP_201_CREATED)
        else:
            return Response(form.errors, status=HTTP_400_BAD_REQUEST)
#Hay que añadir vista de cerrar sesión, el main donde se lanza todo y una clase para la vista de login.