# notifications/urls.py
from django.urls import path
from .views import NotificationListView, mark_notification_read

urlpatterns = [
    path("", NotificationListView.as_view(), name="notifications-list"),
    path("<int:pk>/mark-read/", mark_notification_read, name="notifications-mark-read"),
]
