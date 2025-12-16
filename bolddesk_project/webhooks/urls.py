from django.urls import path
from .views import bolddesk_webhook

urlpatterns = [
    path("bolddesk/", bolddesk_webhook),
]
