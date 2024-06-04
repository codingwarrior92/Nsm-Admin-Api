from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status

from keywords.models import Keywords
from keywords.serializers import KeywordSerializer

# Create your views here.
class KeywordListView(APIView):
    serializer_class = KeywordSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response('OK'),
            400: openapi.Response('Bad Request'),
            403: openapi.Response('Forbidden'),
        }
    )
    def get(self, request, *args, **kwargs):
        keywords = Keywords.objects.all()
        serializer = self.serializer_class(keywords, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class KeywordCreateView(APIView):
    serializer_class = KeywordSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING),
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
        keyword = Keywords(**data)
        keyword.save()
        serializer = self.serializer_class(keyword)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class KeywordUpdateView(APIView):
    serializer_class = KeywordSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING),
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
        keyword = Keywords.objects.get(pk=pk)
        keyword.title = data['title']
        keyword.save()
        serializer = self.serializer_class(keyword)
        return Response(serializer.data, status=status.HTTP_200_OK)

class KeywordDeleteView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response('OK'),
            400: openapi.Response('Bad Request'),
            403: openapi.Response('Forbidden'),
        }
    )
    def delete(self, request, pk, **kwargs):
        Keywords.objects.get(pk=pk).delete()
        return Response({'type': 'success', 'message': 'removed successfully', 'client_id': pk}, status=status.HTTP_200_OK)