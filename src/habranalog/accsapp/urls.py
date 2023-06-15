
from django.urls import path
from accsapp.views import *
app_name='accsapp'
urlpatterns=[
    path('sign-up/',signup,name='signup'),
    path('sign-in/',signin,name='signin'),
    path('sign-out/',signout,name='signout'),
    path('profile/',profile,name='profile')
]