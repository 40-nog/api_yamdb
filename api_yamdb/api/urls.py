from api import views
from django.urls import include, path
from rest_framework import routers

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('auth/signup', views.UserSignup)
router_v1.register(r'users', views.UserViewSet, basename='users')
router_v1.register(
    'users/me',
    views.MyProfileViewSet,
    basename='profile'
)
router_v1.register('titles', views.TitleViewSet, basename='titles')
router_v1.register(r'categories', views.CategoryViewSet, basename='categories')
router_v1.register(r'genres', views.GenreViewSet, basename='genres')
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
    path('v1/auth/token/', views.get_tokens_for_user, name='token')
]
