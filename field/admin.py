
from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Districts, Mandals, NewFieldModel, IndicesModel, CropDetail, CropNdvi


admin.site.register(Mandals, admin.GeoModelAdmin)


# class CropDetailInline(admin.TabularInline):
#     model = CropDetail


# @admin.register(Field)
# class FieldAdmin(LeafletGeoAdmin):
#     inlines = [CropDetailInline]


# class CropNdviInline(admin.TabularInline):
#     model = CropNdvi


# @admin.register(CropDetail)
# class CropAdmin(admin.ModelAdmin):
#     list_display = ['field', 'crop_type', 'crop_status']
#     inlines = [CropNdviInline]


class IndicesModelInline(admin.TabularInline):
    model = IndicesModel


@admin.register(NewFieldModel)
class NewFieldModel(LeafletGeoAdmin):
    list_display = ['farmer', 'village', 'crop']
    inlines = [IndicesModelInline]
