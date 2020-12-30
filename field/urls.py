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

    # indices
    path('indices/', views.indiceshome, name='indices'),
    path('about/', views.about, name='about'),

    # general crop details
    path('detailct/', views.crop_details, name='detailct'),
    path('detailloc/', views.village_details, name='detailloc'),
    path('idetail/', views.individual_deatil, name='idetail'),\

    # registrations
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),

    # crop analysis
    path('analysis/', views.analysis, name='analysis'),
    path('stresscrops/', views.stressed_crops, name='stresscrops'),
    path('timeseries/', views.timeseries, name='timeseries'),
    path('compare/', views.BaseLineChartView.as_view(), name='compare')



]
