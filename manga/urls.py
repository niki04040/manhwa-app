from django.urls import path
from .views import (
    ManhwaListView,
    ManhwaDetailView,
    manhwa_chapters,
    chapter_detail,
    chapter_pages, ManhwaCommentsView,
)

urlpatterns = [
    path('', ManhwaListView.as_view(), name='manhwa-list'),
    path('<int:pk>/', ManhwaDetailView.as_view(), name='manhwa-detail'),
    path('<int:manhwa_id>/chapters/', manhwa_chapters, name='manhwa-chapters'),
    path('chapters/<int:chapter_id>/', chapter_detail, name='chapter-detail'),
    path('chapters/<int:chapter_id>/pages/', chapter_pages, name='chapter-pages'),
    path('manhwa/<int:id>/comments/',ManhwaCommentsView.as_view()),
]