from django.shortcuts import redirect, render
from rest_framework import generics ,status , permissions , serializers
from django.contrib.auth.models import User
from .serializers import RegistrationSerializer, UserSerializer
from rest_framework.response import Response
import uuid
from django.contrib.sessions.models import Session
import jwt
from django.conf import settings
from django.http import HttpResponseRedirect
def generate_access_token(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
        # Ajoutez d'autres données pertinentes à votre access token si nécessaire
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


from django.shortcuts import redirect

class RegistrationAPIView(generics.GenericAPIView):

    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        access_token = generate_access_token(user)
        request.session['access_token'] = access_token

        if serializer.is_valid():
            serializer.save()
            # Redirection explicite vers la page d'accueil du microservice de produits
            return HttpResponseRedirect('http://127.0.0.1:8001/products/')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        # Vérifier la présence et la validité du token d'accès dans la session
        access_token = request.session.get('access_token')
        if access_token:
            try:
                # Vérifier la validité du token
                payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
                # Si le token est valide, autoriser l'accès au service des produits
                return super().get(request, *args, **kwargs)
            except jwt.exceptions.InvalidTokenError:
                # Si le token est invalide, renvoyer une erreur d'authentification
                return Response({'error': 'Invalid access token'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Si le token n'est pas présent, renvoyer une erreur d'authentification
            return Response({'error': 'No access token found'}, status=status.HTTP_401_UNAUTHORIZED)