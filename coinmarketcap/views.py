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
class GetInfoParametersSerializer(serializers.Serializer):
    uuid = serializers.CharField(help_text="UUID of the coin you want to request.")
    referenceCurrencyUuid = serializers.CharField(required=False, default='yhjMzLPhuIDl', help_text="UUID of reference currency, in which all the prices are calculated. Defaults to US Dollar")
    timePeriod = serializers.CharField(required=False, default='24h', help_text="Time period where the change and sparkline are based on")
class CryptocurrencyInfo(APIView):
    @swagger_auto_schema(query_serializer=GetInfoParametersSerializer())
    def get(self, request, *args, format=None):
        serializer = GetInfoParametersSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        data = serializer.validated_data
        # url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/category'
        uuid = data['uuid']
        url = f'https://api.coinranking.com/v2/coin/{uuid}'
        parameters = {
            'referenceCurrencyUuid': data['referenceCurrencyUuid'],
            'timePeriod': data['timePeriod']
        }
        headers = {
            'x-access-token': settings.COINRANKING_API_KEY,
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            if data.get('status', {}) == 'fail':
                return Response({'type': 'failure', 'error_message': data['status']['error_message']}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data, status=status.HTTP_200_OK)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return Response({"type": "failure", "detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        
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