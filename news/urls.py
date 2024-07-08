from django.urls import path
from .views import PostList, PostDetail, NewsSearch

urlpatterns = [
    path('', PostList.as_view(), name='posts'),
    path('<int:pk>', PostDetail.as_view(), name='news_detail'),
    path('search/', NewsSearch.as_view(), name='news_search'),
]