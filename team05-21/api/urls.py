from django.urls import path

from api.viewsaccounts import UserViewSet
from api.viewsprofile import ProfileViewSet
from api.viewsvideos import VideoViewSet
from api.viewsvideos import CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', UserViewSet, 'User')
router.register('profile', ProfileViewSet, 'Profile')
router.register('video', VideoViewSet, 'Video')
router.register('comment', CommentViewSet, 'Comment')

urlpatterns = router.urls
