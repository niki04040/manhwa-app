from rest_framework import serializers
from .models import Bookmark, ReadingProgress
from manga.models import Manhwa, Chapter


class BookmarkSerializer(serializers.ModelSerializer):
    manhwa_id = serializers.IntegerField(source='manhwa.id', read_only=True)
    title = serializers.CharField(source='manhwa.title', read_only=True)
    cover = serializers.URLField(source='manhwa.cover_image', read_only=True)
    added_at = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Bookmark
        fields = ['id', 'manhwa_id', 'title', 'cover', 'added_at']
        read_only_fields = ['user']


class ReadingProgressSerializer(serializers.ModelSerializer):
    manhwaId = serializers.IntegerField(source='manhwa.id', read_only=True)
    chapterId = serializers.IntegerField(source='chapter.id', read_only=True)
    pageIndex = serializers.IntegerField(source='page_index')
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = ReadingProgress
        fields = ['manhwaId', 'chapterId', 'pageIndex', 'updatedAt']
        read_only_fields = ['user']