from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status

from client.models import Client
from client.serializers import ClientSerializer

# Create your views here.
class ClientListView(APIView):
    serializer_class = ClientSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response('OK'),
            400: openapi.Response('Bad Request'),
            403: openapi.Response('Forbidden'),
        }
    )
    def get(self, request, *args, **kwargs):
        clients = Client.objects.all()
        serializer = self.serializer_class(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ClientCreateView(APIView):
    serializer_class = ClientSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'twitter_id': openapi.Schema(type=openapi.TYPE_STRING),
                'website': openapi.Schema(type=openapi.TYPE_STRING),
                'telegram_id': openapi.Schema(type=openapi.TYPE_STRING),
                'twitter_followers': openapi.Schema(type=openapi.TYPE_INTEGER),
                'telegram_subscribers': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        responses={
            200: openapi.Response('OK'),
            400: openapi.Response('Bad Request'),
            403: openapi.Response('Forbidden'),
        }
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        client = Client(**data)
        client.save()
        serializer = self.serializer_class(client)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ClientUpdateView(APIView):
    serializer_class = ClientSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'twitter_id': openapi.Schema(type=openapi.TYPE_STRING),
                'website': openapi.Schema(type=openapi.TYPE_STRING),
                'telegram_id': openapi.Schema(type=openapi.TYPE_STRING),
                'twitter_followers': openapi.Schema(type=openapi.TYPE_INTEGER),
                'telegram_subscribers': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        responses={
            200: openapi.Response('OK'),
            400: openapi.Response('Bad Request'),
            403: openapi.Response('Forbidden'),
        }
    )
    def put(self, request, pk, **kwargs):
        data = request.data
        client = Client.objects.get(pk=pk)
        client.name = data['name']
        client.twitter_id = data['twitter_id']
        client.website = data['website']
        client.telegram_id = data['telegram_id']
        client.twitter_followers = data['twitter_followers']
        client.telegram_subscribers = data['telegram_subscribers']
        client.save()
        serializer = self.serializer_class(client)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ClientDeleteView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response('OK'),
            400: openapi.Response('Bad Request'),
            403: openapi.Response('Forbidden'),
        }
    )
    def delete(self, request, pk, **kwargs):
        Client.objects.get(pk=pk).delete()
        return Response({'type': 'success', 'message': 'removed successfully', 'client_id': pk}, status=status.HTTP_200_OK)