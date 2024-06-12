from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from coinmarketcap.models import Crypto
from coinmarketcap.serializers import CryptoSerializer
import json

# Create your views here.
class CryptocurrencyInfo(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Response('OK'),
            400: openapi.Response('Bad Request'),
            403: openapi.Response('Forbidden'),
        }
    )
    def post(self, request, *args, format=None):
        data = request.data # holds username and password (in dictionary)
        url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info'
        parameters = {
            'id': data["id"],
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': settings.COINRANKING_API_KEY,
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            if data['status']['error_code'] == 400:
                return Response({'type':'failure', 'error_message': data['status']['error_message']}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'type':'success', 'data': data}, status=status.HTTP_200_OK)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return Response({"type": "failure", "detail": e}, status=status.HTTP_403_FORBIDDEN)

# class CryptocurrencyMap(APIView):
#     @swagger_auto_schema(
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'listing_status': openapi.Schema(type=openapi.TYPE_STRING, default='active'),
#                 'start': openapi.Schema(type=openapi.TYPE_INTEGER, default='1'),
#                 'limit': openapi.Schema(type=openapi.TYPE_INTEGER, default='5000'),
#                 'sort': openapi.Schema(type=openapi.TYPE_STRING, default='cmc_rank'),
#                 'aux': openapi.Schema(type=openapi.TYPE_STRING, default='platform,first_historical_data,last_historical_data,is_active'),
#             },
#         ),
#         responses={
#             200: openapi.Response('OK'),
#             400: openapi.Response('Bad Request'),
#             403: openapi.Response('Forbidden'),
#         }
#     )
#     def post(self, request, *args, format=None):
#         data = request.data # holds username and password (in dictionary)
#         url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
#         parameters = {
#             'listing_status': data['listing_status'],
#             'start': data['start'],
#             'limit': data['limit'],
#             'sort': data['sort'],
#             'aux': data['aux'],
#         }
#         headers = {
#             'Accepts': 'application/json',
#             'X-CMC_PRO_API_KEY': settings.COINMARKET_API_KEY,
#         }

#         session = Session()
#         session.headers.update(headers)

#         try:
#             response = session.get(url, params=parameters)
#             data = json.loads(response.text)
#             print (data)
#             if data['status']['error_code'] == 400:
#                 return Response({'type':'failure', 'error_message': data['status']['error_message']}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response({'type':'success', 'data': data}, status=status.HTTP_200_OK)
#         except (ConnectionError, Timeout, TooManyRedirects) as e:
#             return Response({"type": "failure", "detail": e}, status=status.HTTP_403_FORBIDDEN)
        
# class CryptocurrencyCategories(APIView):
#     @swagger_auto_schema(
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'start': openapi.Schema(type=openapi.TYPE_INTEGER),
#                 'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
#                 'id': openapi.Schema(type=openapi.TYPE_STRING),
#                 'slug': openapi.Schema(type=openapi.TYPE_STRING),
#                 'symbol': openapi.Schema(type=openapi.TYPE_STRING),
#             },
#         ),
#         responses={
#             200: openapi.Response('OK'),
#             400: openapi.Response('Bad Request'),
#             403: openapi.Response('Forbidden'),
#         }
#     )
#     def post(self, request, *args, format=None):
#         data = request.data # holds username and password (in dictionary)
#         url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/categories'
#         parameters = {
#             # 'listing_status': data['listing_status'],
#             'start': data['start'],
#             'limit': data['limit'],
#             # 'slug': data['slug'],
#             # 'aux': data['aux'],
#         }
#         headers = {
#             'Accepts': 'application/json',
#             'X-CMC_PRO_API_KEY': settings.COINMARKET_API_KEY,
#         }

        session = Session()
        session.headers.update(headers)

#         try:
#             response = session.get(url, params=parameters)
#             data = json.loads(response.text)
#             print (data)
#             if data['status']['error_code'] == 400:
#                 return Response({'type':'failure', 'error_message': data['status']['error_message']}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response({'type':'success', 'data': data}, status=status.HTTP_200_OK)
#         except (ConnectionError, Timeout, TooManyRedirects) as e:
#             return Response({"type": "failure", "detail": e}, status=status.HTTP_403_FORBIDDEN)
        
class GetParametersSerializer(serializers.Serializer):
    start = serializers.IntegerField(help_text="Start index for pagination")
    limit = serializers.IntegerField(help_text="Number of results to return")
    keyword = serializers.CharField(required=False, default='')
class CryptocurrencyCategory(APIView):
    # Apply the swagger_auto_schema decorator without specifying the method
    @swagger_auto_schema(query_serializer=GetParametersSerializer())
    def get(self, request, *args, **kwargs):
        serializer = GetParametersSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        # url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/category'
        url = 'https://api.coinranking.com/v2/coins'
        parameters = {
            # 'id': '6051a82566fc1b42617d6dc6',
            # 'start': data['start'],
            # 'limit': data['limit'],
            'offset': data['start'],
            'limit': data['limit'],
            'tags': 'meme',
            'orderBy': 'marketCap',
            'search': data['keyword']
        }
        headers = {
            # 'Accept': 'application/json',
            # 'X-CMC_PRO_API_KEY': settings.COINRANKING_API_KEY,
            'x-access-token': settings.COINRANKING_API_KEY,
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            print(data)
            if data.get('status', {}) == 'fail':
                return Response({'type': 'failure', 'error_message': data['status']['error_message']}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data, status=status.HTTP_200_OK)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return Response({"type": "failure", "detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

class UpdateCryptocurrency(APIView):
    serializer_class = CryptoSerializer
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['coin_id'],
            properties={
                'coin_id': openapi.Schema(type=openapi.TYPE_STRING),
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
        try:
            Crypto.objects.get(coin_id=data['coin_id']).delete()
        except Crypto.DoesNotExist:
            coin = Crypto(**data)
            coin.save()

        coins = Crypto.objects.all()
        serializer = self.serializer_class(coins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetCryptocurrencyList(APIView):
    serializer_class = CryptoSerializer
    @swagger_auto_schema(
        responses={
            200: openapi.Response('OK'),
            400: openapi.Response('Bad Request'),
            403: openapi.Response('Forbidden'),
        }
    )
    def get(self, request, *args, format=None):
        coins = Crypto.objects.all()
        serializer = self.serializer_class(coins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)