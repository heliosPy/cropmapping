from django.urls import path
from . import views

app_name = 'field'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('allcrops/', views.allcrops, name='allcrops'),
    path('rice/', views.ricecrop, name='rice'),
    path('cotton/', views.cottoncrop, name='cotton'),
    path('mango/', views.mangocrop, name='mango'),
    path('maize/', views.maizecrop, name='maize'),
    path('veg/', views.vegcrop, name='veg'),
    path('others/', views.othercrop, name='others'),
    path('count/', views.featureCount, name='count'),
    path('indices/', views.indiceshome, name='indices'),
    path('about/', views.about, name='about'),
    path('detailct/', views.crop_details, name='detailct'),
    path('idetail/', views.individual_deatil, name='idetail'),


]
