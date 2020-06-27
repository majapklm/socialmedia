from django.urls import re_path
from .views import *



urlpatterns = [

    re_path(r'^list/', PostListViewSet.as_view(), name='Api to list all posts for users'),
    re_path(r'^(?P<post_id>[\w|\W]+)/action/$', PostActionViewSet.as_view(), name='Api to list or like/dislike a particular post'),
]