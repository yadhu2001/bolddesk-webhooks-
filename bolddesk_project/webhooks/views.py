# views.py
import base64, hashlib, hmac, json
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import BoldDeskWebhookEvent

@csrf_exempt
def bolddesk_webhook(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")

    raw_bytes = request.body
    raw_text = raw_bytes.decode("utf-8", errors="replace")

    # 1) Read headers
    event_type = request.headers.get("Event-Type", "")
    signature = request.headers.get("x-signature", "")

    # 2) Verify signature if enabled in BoldDesk
    # BoldDesk signing: HMAC-SHA256 + Base64 in x-signature :contentReference[oaicite:5]{index=5}
    secret = getattr(settings, "BOLDDESK_WEBHOOK_SECRET", None)
    if secret and signature:
        expected = base64.b64encode(
            hmac.new(secret.encode("utf-8"), raw_bytes, hashlib.sha256).digest()
        ).decode("utf-8")
        if not hmac.compare_digest(signature, expected):
            return HttpResponseForbidden("Bad signature")

    # 3) Parse body based on Content-Type
    content_type = request.headers.get("Content-Type", "")
    data = None

    if "application/json" in content_type or raw_text.strip().startswith("{"):
        try:
            data = json.loads(raw_text)
        except Exception:
            return HttpResponseBadRequest("Invalid JSON")

    # If you chose XML in BoldDesk, parse XML here (example)
    # elif "xml" in content_type:
    #     import xmltodict
    #     data = xmltodict.parse(raw_text)

    # 4) Store raw event (so nothing is lost)
    BoldDeskWebhookEvent.objects.create(
        event_type=event_type,
        signature=signature,
        raw_body=data if isinstance(data, dict) else None,
        raw_text=raw_text,
    )

    # 5) Then map to your own tables (example pseudo)
    # if event_type == "Ticket Created":
    #     upsert_ticket_from_bolddesk(data)

    return JsonResponse({"ok": True})
