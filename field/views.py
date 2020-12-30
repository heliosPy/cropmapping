from chartjs.views.lines import BaseLineChartView
from django.shortcuts import render, redirect
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from . models import NewFieldModel, IndicesModel
from .util import returndataset
from .forms import UserForm, UserLoginForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Avg
from datetime import datetime
from decimal import Decimal


def homepage(request):
    total = NewFieldModel.objects.count()
    return render(request, 'field/home.html', {'total': total})


def allcrops(request):
    if request.is_ajax():
        data = serialize('geojson', NewFieldModel.objects.all())
        return HttpResponse(data, content_type='geojson')


def ricecrop(request):
    if request.is_ajax():
        data = serialize('geojson', NewFieldModel.objects.filter(crop='Rice'))
        return HttpResponse(data,)


def maizecrop(request):
    if request.is_ajax():
        return returndataset('Maize')


def mangocrop(request):
    if request.is_ajax():
        return returndataset('Mango')


def vegcrop(request):
    if request.is_ajax():
        return returndataset('Vegetables')


def cottoncrop(request):
    if request.is_ajax():
        return returndataset('Cotton')


def othercrop(request):
    if request.is_ajax():
        return returndataset('Others')


def featureCount(request):
    if request.is_ajax():
        crop = request.GET.get('crop')
        print(crop)
        try:
            total = NewFieldModel.objects.filter(crop=crop).count()
        except NewFieldModel.DoesNotExist:
            total = 'Wrong Qurey'
        return JsonResponse({'total': total})


@login_required
def indiceshome(request):
    return render(request, 'field/indices.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('field:home')


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('field:indices')
        return render(request, 'field/login.html', {'loginform': form})
    form = UserLoginForm()
    return render(request, 'field/login.html', {'loginform': form})


def user_register(request):
    if request.method == "POST":
        userre = UserForm(request.POST)
        if userre.is_valid():
            userre.save()
            return redirect('field:login')
        else:
            return render(request, 'field/registration.html', {'user': userre})

    userre = UserForm()
    return render(request, 'field/registration.html', {'user': userre})


def about(request):
    return render(request, 'field/about.html')


def office(request):
    return render(request, 'field/office.html')


@login_required
def crop_details(request):
    crop_type = request.GET.get('crop_type')
    try:
        data = NewFieldModel.objects.filter(crop=crop_type)
    except NewFieldModel.DoesNotExist:
        message.error(request, f'There are no fields of {crop_type}')
        return redirect('field:indices')
    return render(request, 'field/details.html', {'data': data, 'type': crop_type, })


@login_required
def individual_deatil(request):
    id = request.GET.get('uid')
    try:
        data = NewFieldModel.objects.prefetch_related('ndvi_values').get(id=id)
        ndvi = IndicesModel.objects.filter(crop=data)
    except NewFieldModel.DoesNotExist:
        return redirect('field:indices')
    ndvi_value_over_time = []
    lables = []
    for i in ndvi:
        ndvi_value_over_time.append(float(i.value))
        lables.append(datetime.strftime(i.date, '%d/%m'))

    return render(request, 'field/idetails.html', {'data': data, 'ndvi': ndvi, 'search_crop': True, 'ndvit': ndvi_value_over_time, 'labels': lables})


@login_required
def village_details(request):
    village = request.GET.get('village')
    try:
        data = NewFieldModel.objects.filter(village=village)
    except NewFieldModel.DoesNotExist:
        message.error(request, f'There are no fields in the {village} village')
        return redirect('field:indices')
    return render(request, 'field/details.html', {'data': data, 'type': village, })


@login_required
def analysis(request):
    return render(request, 'field/analysis.html')


@login_required
def stressed_crops(request):
    date = request.GET.get('date')
    date = '2020/' + date[0:2] + '/' + date[2:]

    pdate = datetime.strptime(date, "%Y/%m/%d").date()
    crop = request.GET.get('crop_type')
    try:
        avg = IndicesModel.objects.filter(
            date=pdate, crop__crop=crop).aggregate(avg_ndvi=Avg('value'))
        ndvi_avg = avg['avg_ndvi']
        if ndvi_avg:
            # need the values less than avg - 0.1
            tolernet_ndvi_avg = ndvi_avg - Decimal(0.1)

            # selecting the indices records whose value less than tolerated avg for that crop and date
            data = IndicesModel.objects.select_related('crop').filter(
                crop__crop=crop,
                value__lt=tolernet_ndvi_avg,
                date=pdate)
        else:
            data = None
    except NewFieldModel.DoesNotExist:
        return redirect('field:analysis')
    return render(request, 'field/result.html', {'data': data, 'avg': ndvi_avg, 'date': date, 'crop': crop})


@login_required
def timeseries(request):
    id = request.GET.get('uid')
    try:
        data = NewFieldModel.objects.get(id=id)
        ndvi = IndicesModel.objects.filter(crop=data)
    except NewFieldModel.DoesNotExist:
        return redirect('field:analysis')
    ndvi_value_over_time = []
    lables = []
    avg_ndvi = []
    for i in ndvi:
        avg = IndicesModel.objects.filter(
            date=i.date, crop__crop=i.crop.crop).aggregate(avg_ndvi_value=Avg('value'))
        avg_value = avg['avg_ndvi_value']
        avg_ndvi.append(float("{:.3f}".format(avg_value)))
        ndvi_value_over_time.append(float(i.value))
        lables.append(datetime.strftime(i.date, '%d/%m'))

    return render(request, 'field/timeseries.html', {'data': data, 'ndvi': ndvi_value_over_time, 'avg_ndvi': avg_ndvi, 'labels': lables})
