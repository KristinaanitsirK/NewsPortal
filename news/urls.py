from django.urls import path
from .views import (PostList, PostDetail, PostSearch,
                    PostCreate, PostUpdate, PostDelete,
                    subscriptions)

urlpatterns = [
    path('news/', PostList.as_view(), name='posts'),
    path('news/<int:pk>', PostDetail.as_view(), name='news_detail'),
    path('news/search/', PostSearch.as_view(), name='news_search'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('article/create/', PostCreate.as_view(), name='article_create'),
    path('news/<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
    path('article/<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('article/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]