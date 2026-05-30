from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Manhwa(models.Model):
    STATUS_CHOICES = (
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    cover_image = models.URLField(max_length=500)
    banner_image = models.URLField(max_length=500, blank=True, null=True)  # بنر (تصویر بزرگ هدر)
    is_popular = models.BooleanField(default=False)  # برای بخش محبوب‌ترین‌ها
    is_trending = models.BooleanField(default=False)  # برای بخش جدیدترین‌ها یا داغ‌ها
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    rating = models.FloatField(default=0.0)  # میانگین امتیاز
    genres = models.ManyToManyField(Genre, related_name='manhwas')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Chapter(models.Model):

    manhwa = models.ForeignKey(
        Manhwa,
        on_delete=models.CASCADE,
        related_name='chapters'
    )

    title = models.CharField(max_length=255)

    chapter_number = models.FloatField()

    pdf = models.FileField(
        upload_to='chapters/pdfs/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['chapter_number']

    def __str__(self):
        return f"{self.manhwa.title} - Chapter {self.chapter_number}"

class ChapterPage(models.Model):
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name='pages'
    )

    image = models.ImageField(
        upload_to='chapters/pages/'
    )
    page_index = models.PositiveIntegerField()

    class Meta:
        ordering = ['page_index']

    def __str__(self):
        return f"Page {self.page_index}"

class Comment(models.Model):

    manhwa = models.ForeignKey(
        Manhwa,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    username = models.CharField(max_length=100)

    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.manhwa.title}"