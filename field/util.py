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


# before loading this function import datetime, csv, NewFieldModel
# and IndicesModel
# pass the csv file path with respect to basedir as csv_file_name
def load_ndvi_data_to_database(csv_file_name, NewFieldModel, IndicesModel):
    import csv
    import datetime
    file = open(csv_file_name, 'r')
    csv_reader = csv.DictReader(file)
    line_c = 0
    for row in csv_reader:
        if line_c == 0:
            line_c = 1
        else:
            farmer = row['Farmer']
            crop = row['Crop']
            village = row['Village']
            try:
                cropp = NewFieldModel.objects.get(
                    farmer=farmer, crop=crop, village=village)
            except NewFieldModel.DoesNotExist:
                continue
            name = 'NDVI'
            value = row['NDVI']
            date = datetime.datetime.strptime(row['Date'], "%Y-%m-%d").date()
            IndicesModel.objects.create(
                name=name, crop=cropp, date=date, value=value)
