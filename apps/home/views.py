# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import datetime
import json
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse

from auto.models import Auto
from datas.models import Data
from devices.models import Device
from hengio.models import Hengio


def index(request):
    sensors = Device.objects.filter(type=2)
    relays = Device.objects.filter(type=1)
    autos =Auto.objects.all()
    autos_on = Auto.objects.filter(auto_status=1).first()
  

    now = datetime.datetime.now()
    seven_days_ago = now - datetime.timedelta(days=4)
    
    data_v7 = Data.objects.filter(pin='V7', date__gte=seven_days_ago).values('value', 'date')
    data_v8 = Data.objects.filter(pin='V8', date__gte=seven_days_ago).values('value', 'date')
    data_v4 = Data.objects.filter(pin='V4', date__gte=seven_days_ago).values('value', 'date')
    data_v5 = Data.objects.filter(pin='V5', date__gte=seven_days_ago).values('value', 'date')

    def serialize_data(data):
        return [{'value': item['value'], 'date': item['date'].isoformat()} for item in data]

    data_list_v7 = serialize_data(data_v7)
    data_list_v8 = serialize_data(data_v8)
    data_list_v4 = serialize_data(data_v4)
    data_list_v5 = serialize_data(data_v5)

    context = {
        'sensors': sensors,
        'relays': relays,
        'autos': autos,
        'autos_on' :autos_on,
        'segment': 'index',
        'data_list_v7': json.dumps(data_list_v7),  # Serialize to JSON
        'data_list_v8': json.dumps(data_list_v8),  # Serialize to JSON
        'data_list_v4': json.dumps(data_list_v4),  # Serialize to JSON
        'data_list_v5': json.dumps(data_list_v5),  # Serialize to JSON
    }
    
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


def addgio(request):
    if request.method == "POST":

        api_key = request.POST.get("api_key")
        pin = request.POST.get("pin")
        name = request.POST.get("name")
        status = request.POST.get("status")
        trigger_time = request.POST.get("trigger_time")
        days_of_week = request.POST.getlist("days_of_week")

        


        response_data = {
            "api_key": api_key,
            "pin": pin,
            "name": name,
            "status": status,
            "trigger_time": trigger_time,
            "days_of_week": days_of_week,
        }
        print(response_data)
        hengio = Hengio.objects.create(
                api_key=api_key,
                pin=pin,
                name=name,
                status=status,
                time=trigger_time,
                days_of_week=days_of_week,
            )
        hengio.save()
        return JsonResponse({"success": True}, status=200)

    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)  

def scene(request):
    sensors = Device.objects.filter(type=2)
    relays = Device.objects.filter(type=1)
    hengios = Hengio.objects.all()
    autos =Auto.objects.all()
    context = {
        'sensors': sensors,
        'relays': relays,
        'hengios':hengios,
        'segment': 'index',
        'autos': autos,
    }
    return render(request, 'home/hengio.html', context)

def auto(request):
    sensors = Device.objects.filter(type=2)
    relays = Device.objects.filter(type=1)
    autos =Auto.objects.all()

    context = {
        'sensors': sensors,
        'relays': relays,
        'autos': autos,
        
       
        'segment': 'index',
    }
    return render(request, 'home/auto.html', context)
def chart(request):
    now = datetime.datetime.now()
    print(now)
    seven_days_ago = now - datetime.timedelta(days=4)
    
    # Fetch data for each sensor from the database
    data_v7 = Data.objects.filter(pin='V7', date__gte=seven_days_ago).values('value', 'date')

    for i in range(2):
        print(f"data_list_v7[{i}]: {data_v7[i]}")
    data_v8 = Data.objects.filter(pin='V8', date__gte=seven_days_ago).values('value', 'date')
    data_v4 = Data.objects.filter(pin='V4', date__gte=seven_days_ago).values('value', 'date')
    data_v5 = Data.objects.filter(pin='V5', date__gte=seven_days_ago).values('value', 'date')
    data_v9 = Data.objects.filter(pin='V9', date__gte=seven_days_ago).values('value', 'date')

    # Function to serialize data to JSON format
    def serialize_data(data):
        return [{'value': item['value'], 'date': item['date'].isoformat()} for item in data]

    # Serialize data for each sensor
    data_list_v7 = serialize_data(data_v7)
    data_list_v8 = serialize_data(data_v8)
    data_list_v4 = serialize_data(data_v4)
    data_list_v5 = serialize_data(data_v5)
    data_list_v9 = serialize_data(data_v9)

    for i in range(2):
        print(f"data_list_v7[{i}]: {data_list_v7[i]}")
    # Prepare context for the template
    context = {
        'segment': 'index',
        'data_list_v7': json.dumps(data_list_v7),  # Serialize to JSON
        'data_list_v8': json.dumps(data_list_v8),  # Serialize to JSON
        'data_list_v4': json.dumps(data_list_v4),  # Serialize to JSON
        'data_list_v5': json.dumps(data_list_v5),  # Serialize to JSON
        'data_list_v9': json.dumps(data_list_v9),  # Serialize to JSON
    }
    
    # Load and render the template
    html_template = loader.get_template('home/chart.html')
    return HttpResponse(html_template.render(context, request))

def delete_hengio(request, id):
    hengio = get_object_or_404(Hengio, id=id)
    if request.method == 'DELETE':
        hengio.delete()
        return JsonResponse({'message': 'Đã xóa thành công!'}, status=200)
    return JsonResponse({'message': 'Xóa thất bại!'}, status=400)

def delete_auto(request, id):
    auto = get_object_or_404(Auto, id=id)
    if request.method == 'DELETE':
        auto.delete()
        return JsonResponse({'message': 'Đã xóa thành công!'}, status=200)
    return JsonResponse({'message': 'Xóa thất bại!'}, status=400)

def edit_gio(request):
    if request.method == "POST":
        id =request.POST.get("id")
        hengio = get_object_or_404(Hengio, id=id)
        hengio.api_key = request.POST.get("api_key")
        hengio.api_key = request.POST.get("api_key")
        hengio.pin = request.POST.get("pin")
        hengio.name = request.POST.get("name")
        hengio.status = request.POST.get("status")
        hengio.time = request.POST.get("trigger_time")
        hengio.days_of_week = request.POST.getlist("days_of_week")
        hengio.save()
        return JsonResponse({"success": True}, status=200)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)

def edit_auto_value(request):
    if request.method == "POST":
        id =request.POST.get("id")
        auto =get_object_or_404(Auto, id=id)
        auto_value = request.POST['auto_value']
        auto.auto_status=auto_value
        print(request.POST['auto_value'])

        auto.save()
        return JsonResponse({"success": True}, status=200)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)
def edit_auto(request):
    if request.method == "POST":
        id =request.POST.get("id")
        auto =get_object_or_404(Auto, id=id)

        auto.auto_name = request.POST['auto_name']
        auto.pump_choice = request.POST['pump_choice']
        auto.van_status = request.POST['van_status']
        auto.min_ph = request.POST['min_ph']
        auto.max_ph = request.POST['max_ph']
        auto.min_light = request.POST['min_light']
        auto.save()
        return JsonResponse({"success": True}, status=200)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)
def add_auto(request):
    if request.method == 'POST':
        auto_name = request.POST['auto_name']
        pump_choice = request.POST['pump_choice']
        van_status = request.POST['van_status']
        min_ph = request.POST['min_ph']
        max_ph = request.POST['max_ph']
        min_light = request.POST['min_light']


        Auto.objects.create(
            auto_name=auto_name,
            pump_choice=pump_choice,
            van_status=van_status,
            min_ph=min_ph,
            max_ph=max_ph,
            min_light=min_light,

        )
        return JsonResponse({"success": True}, status=200)

    return render(request, 'add_auto.html')
        
def pages(request):
    context = {}

    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
