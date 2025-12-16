import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import BoldDeskEvent

@csrf_exempt
def bolddesk_webhook(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")

    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    event_type = request.headers.get("Event-Type", "")  # if BoldDesk sends it

    BoldDeskEvent.objects.create(
        event_type=event_type,
        payload=data
    )

    return JsonResponse({"ok": True})

from django.shortcuts import render
from .models import BoldDeskEvent

def events_list(request):
    events = BoldDeskEvent.objects.order_by("-received_at")[:200]  # latest 200

    # We will show key-value table of payload for each event
    return render(request, "webhooks/events_list.html", {"events": events})
