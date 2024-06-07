from django.urls import path
from .views import CryptocurrencyInfo, CryptocurrencyCategory, UpdateCryptocurrency, GetCryptocurrencyList #, CryptocurrencyMap, CryptocurrencyCategories

urlpatterns = [
    path('cryptocurrency/info', CryptocurrencyInfo.as_view(), name='cryptocurrency-info'),
    # path('cryptocurrency/map', CryptocurrencyMap.as_view(), name='cryptocurrency-map'),
    # path('cryptocurrency/categories', CryptocurrencyCategories.as_view(), name='cryptocurrency-categories'),
    path('cryptocurrency/category', CryptocurrencyCategory.as_view(), name='cryptocurrency-category'),
    path('cryptocurrency/update', UpdateCryptocurrency.as_view(), name='update-cryptocurrency'),
    path('cryptocurrency/get', GetCryptocurrencyList.as_view(), name='get-cryptocurrency')
]