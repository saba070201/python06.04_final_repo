from django.urls import path
from articleapp.views import *
app_name='articleapp'
urlpatterns=[
    path('',home,
         name='home'),
    path('view-art-<int:art_id>',view_art,name='view_art'),
    path('create-article/',create_article,name='create_article'),
    path('change-article-<int:art_id>/',change_article,name='change_article'),
    path('view-article-<int:art_id>/',view_article,name='view_article'),
    path('delete-article-<int:art_id>/',delete_article,name='delete_article'),
    # path('change-article-<int:art_id>/create-article-block',change_article,name='change_article'),
    # path('change-article-<int:art_id>/change-article-block-<int:art_id>',change_article,name='change_article'),
]