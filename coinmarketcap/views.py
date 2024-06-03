from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
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
    def post(self, request, user_id, format=None):
        data = request.data # holds username and password (in dictionary)
        url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info'
        parameters = {
            'id': data["id"],
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': settings.COINMARKET_API_KEY,
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            print (data)
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
#     def post(self, request, user_id, format=None):
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
#     def post(self, request, user_id, format=None):
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
        
class CryptocurrencyCategory(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'start': openapi.Schema(type=openapi.TYPE_INTEGER, default='1'),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, default='100'),
                # 'id': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Response('OK'),
            400: openapi.Response('Bad Request'),
            403: openapi.Response('Forbidden'),
        }
    )
    def post(self, request, user_id, format=None):
        data = request.data # holds username and password (in dictionary)
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/category'
        parameters = {
            'id': '6051a82566fc1b42617d6dc6',
            'start': data['start'],
            'limit': data['limit'],
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': settings.COINMARKET_API_KEY,
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            print (data)
            if data['status']['error_code'] == 400:
                return Response({'type':'failure', 'error_message': data['status']['error_message']}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'type':'success', 'data': data}, status=status.HTTP_200_OK)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return Response({"type": "failure", "detail": e}, status=status.HTTP_403_FORBIDDEN)