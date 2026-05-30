from django.contrib import admin
from .models import Manhwa, Chapter, ChapterPage, Genre   # Genre را هم import کن

class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class ManhwaAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'rating', 'is_popular', 'is_trending', 'created_at','chapter_count')
    list_filter = ('status', 'is_popular', 'is_trending', 'genres')
    search_fields = ('title',)
    filter_horizontal = ('genres',)   # یک کادر جذاب برای انتخاب ژانرها
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'cover_image', 'banner_image', 'status')
        }),
        ('ویژگی‌ها', {
            'fields': ('is_popular', 'is_trending', 'rating', 'genres')
        }),
    )

    def chapter_count(self, obj):
        return obj.chapters.count()

    chapter_count.short_description = 'تعداد فصل‌ها'  # اسم ستون در ادمین


class ChapterAdmin(admin.ModelAdmin):
    list_display = ['manhwa', 'chapter_number', 'title', 'created_at', 'has_pdf']
    list_filter = ['manhwa']
    search_fields = ['title', 'manhwa__title']

    def has_pdf(self, obj):
        return bool(obj.pdf)

    has_pdf.boolean = True
    has_pdf.short_description = 'PDF آپلود شده؟'

# ثبت مدل‌ها با تنظیمات جدید
admin.site.register(Manhwa, ManhwaAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(ChapterPage)