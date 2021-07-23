from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='product_detail'),
    path('category/<int:pk>', CategoryDetail.as_view(), name='category_detail'),
    path('search', PostsSearch.as_view(), name='product_search'),
    path('create', PostCreate.as_view(), name='product_create'),
    path('update/<int:pk>', PostUpdate.as_view(), name='product_update'),
    path('delete/<int:pk>', cache_page(60*5)(PostDelete.as_view()), name='product_delete'),
    path('become/author/', BecomeAuthor.as_view(), name='become_author'),
    path('upgrade/author/', upgrade_author, name='upgrade_author'),
    path('subscribe/<int:pk>', subscribe_category, name='subscribe_category'),
    path('unsubscribe/<int:pk>', unsubscribe_category, name='unsubscribe_category'),
]
