from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from manga.models import Manhwa, Chapter
from .models import Bookmark, ReadingProgress
from .serializers import BookmarkSerializer, ReadingProgressSerializer


# ➕ Add / List bookmarks
class BookmarkListCreateView(generics.ListCreateAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        manhwa_id = self.request.data.get('manhwaId')
        manhwa = Manhwa.objects.get(id=manhwa_id)
        serializer.save(user=self.request.user, manhwa=manhwa)


# ❌ Remove bookmark
class BookmarkDeleteView(generics.DestroyAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)


# 📌 Save / update reading progress
class ReadingProgressView(generics.CreateAPIView):
    serializer_class = ReadingProgressSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        # دریافت شناسه‌ها از داده ورودی
        manhwa_id = data.get('manhwaId')
        chapter_id = data.get('chapterId')
        page_index = data.get('pageIndex', 0)

        # اعتبارسنجی ساده
        if not manhwa_id or not chapter_id:
            return Response(
                {"error": "manhwaId and chapterId are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            manhwa = Manhwa.objects.get(id=manhwa_id)
            chapter = Chapter.objects.get(id=chapter_id)
        except (Manhwa.DoesNotExist, Chapter.DoesNotExist):
            return Response(
                {"error": "Manhwa or Chapter not found"},
                status=status.HTTP_404_NOT_FOUND
            )

            # ایجاد یا بروزرسانی پیشرفت خواندن
        obj, created = ReadingProgress.objects.update_or_create(
            user=user,
            manhwa=manhwa,
            defaults={
                'chapter': chapter,
                'page_index': page_index
            }
        )
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 📖 Get continue reading
class ContinueReadingView(generics.RetrieveAPIView):
    serializer_class = ReadingProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # آخرین پیشرفت خواندن کاربر (بر اساس updated_at)
        return ReadingProgress.objects.filter(
            user=self.request.user
        ).order_by('-updated_at').first()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({}, status=status.HTTP_204_NO_CONTENT)  # یا 200 با بدنه خالی
        serializer = self.get_serializer(instance)
        return Response(serializer.data)