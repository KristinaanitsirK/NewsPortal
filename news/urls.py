from django.urls import path
from .views import (PostList, PostDetail, PostSearch,
                    PostCreate,
                    )

urlpatterns = [
    path('news/', PostList.as_view(), name='posts'),
    path('news/<int:pk>', PostDetail.as_view(), name='news_detail'),
    path('news/search/', PostSearch.as_view(), name='news_search'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('article/create/', PostCreate.as_view(), name='article_create'),

]