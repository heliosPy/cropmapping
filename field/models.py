
from django.contrib.gis.db import models


class Districts(models.Model):
    geom = models.MultiPolygonField(srid=7756, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    area = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Districts'


class Mandals(models.Model):
    geom = models.MultiPolygonField(srid=7756, blank=True, null=True)
    mandal = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    area = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Mandals'

    def __str__(self):
        return f'{self.mandal}  --- {self.district}'


class Field(models.Model):
    farmer = models.CharField(max_length=50)
    village = models.CharField(max_length=100, blank=True)
    mandal = models.ForeignKey(
        Mandals, on_delete=models.CASCADE, related_name='crop_fields')
    geom = models.MultiPolygonField(srid=7756, blank=True, null=True)

    def __str__(self):
        return self.farmer + " " + self.village


class CropDetail(models.Model):
    CROP_TYPES = (
        ('Rice', 'Rice'),
        ('Vegetables', 'Vegetables'),
        ('Cotton', 'Cotton'),
        ('Maize', 'Maize'),
        ('Cerials', 'Cerials'),
        ('Others', 'Others')
    )
    CROP_STATUS = (
        ('seedling', 'Seedling'),
        ('vegetative', 'Vegetative'),
        ('budding', 'Budding'),
        ('flowering', 'Flowering'),
        ('ripening', 'Ripening'),
        ('Harvested', 'Harvested')
    )

    field = models.ForeignKey(
        Field, on_delete=models.CASCADE, related_name='crops', unique_for_month="created_date")
    crop_type = models.CharField(choices=CROP_TYPES, max_length=30)
    crop_status = models.CharField(choices=CROP_STATUS, max_length=20)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.crop_type} @ {self.field.farmer}'


class Crop50(models.Model):
    geom = models.MultiPolygonField(srid=7756, dim=3, blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    village = models.CharField(max_length=150, blank=True, null=True)
    crop = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crop50'


class Newcrop50(models.Model):
    geom = models.MultiPolygonField(srid=7756, blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    village = models.CharField(max_length=150, blank=True, null=True)
    crop = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'newcrop50'


class CropNdvi(models.Model):
    crop = models.ForeignKey(
        CropDetail, on_delete=models.CASCADE, related_name='ndvi_values')
    date = models.DateField()
    value = models.DecimalField(decimal_places=3, max_digits=4)


class NewFieldModel(models.Model):

    CROP_TYPES = (
        ('Rice', 'Rice'),
        ('Vegetables', 'Vegetables'),
        ('Cotton', 'Cotton'),
        ('Maize', 'Maize'),
        ('Cerials', 'Cerials'),
        ('Others', 'Others')
    )
    farmer = models.CharField(max_length=50)
    village = models.CharField(max_length=100, blank=True)
    mandal = models.ForeignKey(
        Mandals, on_delete=models.CASCADE, related_name='fields')
    geom = models.MultiPolygonField(srid=7756, blank=True, null=True)
    crop = models.CharField(choices=CROP_TYPES, max_length=30)

    def __str__(self):
        return self.farmer + " " + self.village


class IndicesModel(models.Model):
    INDICES_TYPES = (
        ('NDVI', 'NDVI'),
        ("EVI", "EVI"),
        ("LSWI", "LSWI"),
        ('Others', 'Others')
    )
    name = models.CharField(choices=INDICES_TYPES, max_length=10)
    crop = models.ForeignKey(
        NewFieldModel, on_delete=models.CASCADE, related_name='ndvi_values')

    date = models.DateField()
    value = models.DecimalField(decimal_places=3, max_digits=4)

    def __str__(self):
        return self.name + "@" + self.crop.farmer
