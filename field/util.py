from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from .models import NewFieldModel


def returndataset(crop):
    queryset = NewFieldModel.objects.filter(crop=crop)
    data = serialize('geojson', queryset)
    return HttpResponse(data, content_type='geojson')


# this is script to load the ndvi values form csv
#  file = open('ndvi_values.csv', 'r')
#  csv_reader = csv.DictReader(file)
#  line_c = 0
#  for row in csv_reader:
#      if line_c == 0:
#              line_c = 1
#      else:
#              farmer = row['Farmer']
#              crop = row['Crop']
#              village = row['Village']
#              cropp = NewFieldModel.objects.get(farmer=farmer,crop=crop, village=village)
#              name = 'NDVI'
#              value = row['Ndvi']
#              date = datetime.datetime.strptime(row['Date'], '%Y-%m-%d').date()
#              IndicesModel.objects.create(name=name, crop=cropp, date=date, value=value)
