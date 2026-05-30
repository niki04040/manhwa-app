from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from .models import Manhwa ,Chapter,Comment
from .serializers import (
    ManhwaListSerializer,
    ManhwaDetailSerializer,
    ChapterSerializer,
    CommentSerializer,
    ChapterDetailSerializer,
    ChapterPageSerializer
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


@api_view(['GET'])
def manhwa_chapters(request, manhwa_id):
    manhwa = get_object_or_404(Manhwa, pk=manhwa_id)
    chapters = manhwa.chapters.all()  # related_name='chapters'
    serializer = ChapterSerializer(chapters, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def chapter_detail(request, chapter_id):
    """دریافت یک چپتر به همراه صفحات آن"""
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    # اگر نیاز به صفحات دارید، از سریالایزری استفاده کنید که pages را هم داشته باشد
    serializer = ChapterDetailSerializer(chapter, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def chapter_pages(request, chapter_id):
    """فقط صفحات یک چپتر (در صورت نیاز)"""
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    pages = chapter.pages.all()
    serializer = ChapterPageSerializer(pages, many=True)
    serializer = ChapterDetailSerializer(chapter, context={'request': request})
    return Response(serializer.data)


class ManhwaListView(generics.ListAPIView):
    serializer_class = ManhwaListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        search = self.request.GET.get('search')

        queryset = Manhwa.objects.all()

        if search:
            queryset = queryset.filter(title__icontains=search)

        return queryset


class ManhwaDetailView(generics.RetrieveAPIView):
    queryset = Manhwa.objects.all()
    serializer_class = ManhwaDetailSerializer
    permission_classes = [AllowAny]

class ManhwaCommentsView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):

        manhwa_id = self.kwargs['id']

        return Comment.objects.filter(
            manhwa_id=manhwa_id
        ).order_by('-created_at')

    def perform_create(self, serializer):
        manhwa_id = self.kwargs['id']
        # username را از کاربر احراز شده بگیر
        username = self.request.user.username  # اگر از User پیش‌فرض استفاده می‌کنید
        serializer.save(manhwa_id=manhwa_id, username=username)

