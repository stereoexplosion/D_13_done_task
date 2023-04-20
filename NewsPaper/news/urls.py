from django.urls import path
from .views import *
# from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', PostsList.as_view(), name='posts_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='posts_search'),
    path('news/create_news/', NewsCreate.as_view(), name='news_create'),
    path('articles/create_articles/', ArticleCreate.as_view(), name='article_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('articles/<int:pk>/edit/', ArticlesUpdate.as_view(), name='articles_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('author_page/<int:pk>/', AuthorDetail.as_view(), name='author_detail'),
]
