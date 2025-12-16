from django.urls import path
from .views import bolddesk_webhook , events_list

urlpatterns = [
    path("bolddesk/", bolddesk_webhook),
     path("events/", events_list),   
]
