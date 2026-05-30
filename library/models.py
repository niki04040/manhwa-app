from django.conf import settings
from django.db import models

from manga.models import Manhwa, Chapter


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    manhwa = models.ForeignKey(Manhwa, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'manhwa')


class ReadingProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    manhwa = models.ForeignKey(Manhwa, on_delete=models.CASCADE)

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    page_index = models.PositiveIntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'manhwa')