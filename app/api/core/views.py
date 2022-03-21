from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from django.http import HttpResponse


def metrics_view(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)
