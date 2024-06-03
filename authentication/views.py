from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, get_connection
from django.db.models import Sum, F
from django.http import HttpResponse
from django.http import HttpRequest
from django.template import Template, Context
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import views, permissions, status
import json

from .serializers import ObtainTokenSerializer
from authentication.authentication import JWTAuthentication

User = get_user_model()

class UserLoginView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ObtainTokenSerializer
    @swagger_auto_schema(
        request_body=ObtainTokenSerializer,
        responses={
            200: openapi.Response('OK', ObtainTokenSerializer),
            400: openapi.Response('Bad Request'),
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        # password = make_password(serializer.validated_data.get('password'))
        password = serializer.validated_data.get('password')
        user = User.objects.filter(email=email).first()
        
        if user is None:
            return Response({'type': 'failure', 'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(password):
            return Response({'type': 'failure', 'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        # Generate the JWT token
        
        jwt_token = JWTAuthentication.create_jwt(user)
        response_data = json.dumps({
            'type': 'success', 
            'token': jwt_token, 
            'refresh_token': JWTAuthentication.create_jwt(user, True),
            'user_id': user.id,
        }, ensure_ascii=False).encode('utf-8')
        return HttpResponse(response_data, content_type='application/json; charset=utf-8')
    
class UserRegisterView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'email', 'password'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Response('OK'),
            400: openapi.Response('Bad Request'),
            403: openapi.Response('Forbidden'),
        }
    )
    def post(self, request, referr_id=None, format=None):
        data = request.data # holds username and password (in dictionary)
        username = data["name"]
        email = data["email"]

        if username == "" or email == "":
            return Response({"message": "failure", "detail": "username or email cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            check_email =  User.objects.filter(email=email).count()
            check_username =  User.objects.filter(username=username).count()
            if check_email:
                message = "A user with that email address already exist!"
                return Response({"message": "failure", "detail": message}, status=status.HTTP_403_FORBIDDEN)
            elif check_username:
                message = "The username already exist!"
                return Response({"message": "failure", "detail": message}, status=status.HTTP_403_FORBIDDEN)
            else:
                user = {"email": email, "password": make_password(data["password"]), 'username': username, "first_name": username}
                user = User(**user)
                user.save()
                serializer = ObtainTokenSerializer(user)
                return Response({'message':'success', 'user_id': user.id, 'user': serializer.data}, status=status.HTTP_200_OK)
