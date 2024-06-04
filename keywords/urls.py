from django.urls import path
from .views import KeywordListView, KeywordCreateView, KeywordUpdateView, KeywordDeleteView

urlpatterns = [
    path('list', KeywordListView.as_view(), name='keyword_list'),
    path('add', KeywordCreateView.as_view(), name='keyword_new'),
    path('<int:pk>/edit', KeywordUpdateView.as_view(), name='keyword_edit'),
    path('<int:pk>/delete', KeywordDeleteView.as_view(), name='keyword_delete'),
]
