from django.urls import include, path
from rest_framework import routers

from api import views


app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('auth/signup', views.UserSignup)
router_v1.register('users', views.UserViewSet)
router_v1.register(
    'users/me',
    views.MyProfileViewSet,
    basename='profile'
)
router_v1.register('titles', views.TitleViewSet)
router_v1.register('categories', views.CategoryViewSet)
router_v1.register('genres', views.GenreViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
