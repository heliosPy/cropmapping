from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from .models import NewFieldModel


def returndataset(crop):
    queryset = NewFieldModel.objects.filter(crop=crop)
    data = serialize('geojson', queryset)
    return HttpResponse(data, content_type='geojson')
