from rest_framework import viewsets
from .serializers import PostSerializer, TagSerializer, ContactSerailizer
from .models import Post
from rest_framework import permissions
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework import generics
from taggit.models import Tag
from rest_framework.views import APIView
from django.core.mail import send_mail


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    ordering = 'created_at'


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination


class TagDetailView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PageNumberSetPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].lower()
        tag = Tag.objects.get(slug=tag_slug)
        return Post.objects.filter(tags=tag)


class TagView(generics.ListAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [permissions.AllowAny]


class AsideView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-id')[:5]
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]


class FeedBackView(APIView):
    serializer_class = ContactSerailizer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer_class = ContactSerailizer(data=request.data)
        if serializer_class.is_valid():
            data = serializer_class.data
            name = data.get('name')
            from_email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            send_mail(f'От {name} | {subject}', message, from_email, [from_email])
            return Response({"success": "Sent"})
