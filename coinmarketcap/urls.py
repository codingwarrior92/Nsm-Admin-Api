from django.urls import path
from .views import CryptocurrencyInfo, CryptocurrencyCategory #, CryptocurrencyMap, CryptocurrencyCategories

urlpatterns = [
    path('<int:user_id>/cryptocurrency/info/', CryptocurrencyInfo.as_view(), name='cryptocurrency-info'),
    # path('<int:user_id>/cryptocurrency/map/', CryptocurrencyMap.as_view(), name='cryptocurrency-map'),
    # path('<int:user_id>/cryptocurrency/categories/', CryptocurrencyCategories.as_view(), name='cryptocurrency-categories'),
    path('<int:user_id>/cryptocurrency/category/', CryptocurrencyCategory.as_view(), name='cryptocurrency-category'),
]