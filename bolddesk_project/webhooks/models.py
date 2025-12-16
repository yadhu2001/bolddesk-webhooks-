# models.py
from django.db import models

class BoldDeskWebhookEvent(models.Model):
    received_at = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=200, blank=True)
    signature = models.TextField(blank=True)
    raw_body = models.JSONField(null=True, blank=True)  # if JSON
    raw_text = models.TextField(blank=True)            # fallback
