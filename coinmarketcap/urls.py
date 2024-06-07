from django.urls import path
from .views import CryptocurrencyInfo, CryptocurrencyCategory, CryptocurrencyCategories #, CryptocurrencyMap,

urlpatterns = [
    path('cryptocurrency/info/', CryptocurrencyInfo.as_view(), name='cryptocurrency-info'),
    # path('<int:user_id>/cryptocurrency/map/', CryptocurrencyMap.as_view(), name='cryptocurrency-map'),
    path('cryptocurrency/categories/', CryptocurrencyCategories.as_view(), name='cryptocurrency-categories'),
    path('cryptocurrency/category/', CryptocurrencyCategory.as_view(), name='cryptocurrency-category'),
]