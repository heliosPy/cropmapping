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


def indiceshome(request):
    return render(request, 'field/indices.html')


# @login_required
# def user_logout(request):
#     logout(request)
#     return redirect('field:home')


# def user_login(request):
#     if request.method == "POST":
#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = authenticate(username=username, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('field:indices')


def about(request):
    return render(request, 'field/about.html')


def office(request):
    return render(request, 'field/office.html')


def crop_details(request):
    crop_type = request.GET.get('crop_type')
    try:
        data = NewFieldModel.objects.filter(crop=crop_type)
    except NewFieldModel.DoesNotExist:
        message.error(request, 'There are no fields in the given village')
        redirect('field:indices')
    return render(request, 'field/details.html', {'data': data, 'type': crop_type})


def individual_deatil(request):
    id = request.GET.get('uid')
    try:
        data = NewFieldModel.objects.prefetch_related('ndvi_values').get(id=id)
        ndvi = IndicesModel.objects.filter(crop=data)
    except NewFieldModel.DoesNotExist:
        redirect('field:home')

    return render(request, 'field/idetails.html', {'data': data, 'ndvi': ndvi})
