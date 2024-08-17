from django.urls import path
from django.views.decorators.cache import cache_page
from .views import (PostList, PostDetail, PostSearch,
                    PostCreate, PostUpdate, PostDelete,
                    subscriptions, subscribe, CategoryListView)

urlpatterns = [
    path('news/', cache_page(60)(PostList.as_view()), name='posts'),
    path('news/<int:pk>', PostDetail.as_view(), name='news_detail'),
    path('news/search/', cache_page(60)(PostSearch.as_view()), name='news_search'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('article/create/', PostCreate.as_view(), name='article_create'),
    path('news/<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
    path('article/<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('article/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('categories/<int:pk>', cache_page(60 * 5)(CategoryListView.as_view()), name='category_news'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]