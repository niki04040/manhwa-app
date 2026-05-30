from django.urls import path

from .views import (
    BookmarkListCreateView,
    BookmarkDeleteView,
    ReadingProgressView,
    ContinueReadingView
)

urlpatterns = [
    path('favorites/', BookmarkListCreateView.as_view()),
    path('favorites/<int:pk>/', BookmarkDeleteView.as_view()),
    path('progress/', ReadingProgressView.as_view()),
    path('continue/', ContinueReadingView.as_view()),
]