from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, TagDetailView, TagView, AsideView, FeedBackView

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')

urlpatterns = [
    path("", include(router.urls)),
    path("tags/<slug:tag_slug>/", TagDetailView.as_view(), name='tags'),
    path("tags/", TagView.as_view(), name='all_tags'),
    path("aside/", AsideView.as_view(), name='aside'),
    path("feedback/", FeedBackView.as_view()),
]