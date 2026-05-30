from rest_framework import serializers

from .models import Manhwa, Chapter, ChapterPage ,Comment


class ChapterPageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ChapterPage
        fields = ['id', 'image_url', 'page_index']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'title', 'chapter_number']


class ChapterDetailSerializer(serializers.ModelSerializer):
    pages = ChapterPageSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = ['id', 'title', 'chapter_number', 'pages']

class ManhwaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manhwa
        fields = [
            'id',
            'title',
            'cover_image',
            'banner_image',
            'status',
            'is_popular',
            'is_trending',
            'created_at',
            'rating'
        ]


class ManhwaDetailSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True)
    genres = serializers.StringRelatedField(many=True)

    class Meta:
        model = Manhwa
        fields = [
            'id',
            'title',
            'description',
            'cover_image',
            'banner_image',
            'status',
            'chapters',
            'rating',
            'genres'
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'username', 'text', 'created_at', 'manhwa']
        read_only_fields = ['id', 'username', 'created_at', 'manhwa']  # این سه تا فقط برای خروجی