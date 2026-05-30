from io import BytesIO

from django.core.files.base import ContentFile

from pdf2image import convert_from_path

from manga.models import ChapterPage


def convert_pdf_to_pages(chapter):

    if not chapter.pdf:
        return

    pages = convert_from_path(
        chapter.pdf.path,
        dpi=150

    )

    for index, page in enumerate(pages):
        
        page.thumbnail((1080, 1920))

        image_io = BytesIO()
        page.save(image_io, format='WEBP', quality=75, optimize=True)

        image_name = (
            f'chapter_{chapter.id}_page_{index + 1}.jpg'
        )

        chapter_page = ChapterPage(
            chapter=chapter,
            page_index=index + 1  # ← صحیح
        )

        chapter_page.image.save(
            image_name,
            ContentFile(image_io.getvalue()),
            save=True
        )