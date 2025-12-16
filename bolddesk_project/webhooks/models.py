from django.db import models

class BoldDeskEvent(models.Model):
    received_at = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=200, blank=True)
    payload = models.JSONField()   # stores the full BoldDesk JSON

    def __str__(self):
        return f"{self.event_type or 'bolddesk'} @ {self.received_at}"
