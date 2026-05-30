from django.db.models.signals import post_save

from django.dispatch import receiver

from .models import Chapter

from .services.pdf_converter import (
    convert_pdf_to_pages
)


@receiver(post_save, sender=Chapter)
def auto_convert_pdf(
    sender,
    instance,
    created,
    **kwargs
):

    if instance.pdf:

        if instance.pages.count() == 0:

            convert_pdf_to_pages(instance)