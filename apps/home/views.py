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
from apikey.models import APIKey
from mqtt_app.mqtt_client import connect_mqtt
import json
import logging
from mqtt_app.mqtt_client import publish_message  # Sửa tên hàm nếu cần
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
logger = logging.getLogger(__name__)
def index(request):
    # Lấy danh sách thiết bị theo loại và người dùng hiện tại
    sensors = Device.objects.filter(type=2, user=request.user)
    relays = Device.objects.filter(type=1, user=request.user)

    # Lấy API key của người dùng hiện tại
    api_key = get_object_or_404(APIKey, user=request.user).api_key

    context = {
        'sensors': sensors,
        'relays': relays,
        'segment': 'index',
        'api_key': api_key  # Thêm API key vào context
    }
    
    return render(request, 'home/index.html', context)
def listdevice(request):
    # Lấy API key của người dùng hiện tại
    api_key = get_object_or_404(APIKey, user=request.user).api_key

    user = request.user

    # Lọc thiết bị theo user hiện tại
    devices = Device.objects.filter(user=user)

    # Lấy danh sách các PIN đang được sử dụng
    used_pins = Device.objects.filter(user=user).values_list('pin', flat=True)

    # Tạo danh sách giá trị từ V0 đến V50
    all_pins = [f'V{i}' for i in range(51)]

    # Loại trừ các PIN đã được sử dụng
    available_pins = [pin for pin in all_pins if pin not in used_pins]
    
    context = {
        'api_key': api_key,
        'devices': devices,
        'available_pins': available_pins,
    }

    return render(request, 'home/listdevice.html', context)


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
   
    seven_days_ago = now - datetime.timedelta(days=4)
    
    # Fetch data for each sensor from the database
    data_v7 = Data.objects.filter(pin='V1', date__gte=seven_days_ago).values('value', 'date')
    data_v8 = Data.objects.filter(pin='V8', date__gte=seven_days_ago).values('value', 'date')
    data_v4 = Data.objects.filter(pin='V4', date__gte=seven_days_ago).values('value', 'date')
    data_v5 = Data.objects.filter(pin='V1', date__gte=seven_days_ago).values('value', 'date')
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

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_device(request, pin):
    try:
        # Đọc dữ liệu từ body của yêu cầu
        data = json.loads(request.body)
        api_key = data.get('api_key')

        if not api_key:
            return JsonResponse({'message': 'API key is required'}, status=400)

        # Tìm thiết bị dựa trên pin và api_key
        devices = Device.objects.filter(pin=pin, api_key__api_key=api_key)

        if devices.exists():
            for device in devices:
                # Xóa thiết bị trong cơ sở dữ liệu
                device.delete()

            # Xóa topic MQTT tương ứng
            topic = f"API/{api_key}/{pin}/"
            client = connect_mqtt()  # Kết nối MQTT client
            if client:
                client.publish(topic, payload=None, retain=False)
                client.loop_stop()
                return JsonResponse({'message': 'Device deleted successfully'}, status=200)
            else:
                return JsonResponse({'message': 'Failed to connect to MQTT broker'}, status=500)
        else:
            return JsonResponse({'message': 'Device not found or API key mismatch'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

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

@login_required
def add_device(request):
    if request.method == 'POST':
        device = Device()
        device.name = request.POST.get('name')
        device.type = int(request.POST.get('type'))
        device.pin = request.POST.get('pin')
        device.unit = request.POST.get('unit')
        device.user = request.user

        try:
            api_key = APIKey.objects.get(user=request.user)
            device.api_key = api_key
        except APIKey.DoesNotExist:
            pass
        
        device.value = '0'
        device.save()

        topic = f"API/{api_key.api_key}/{device.pin}/"
        payload = {
            'value': device.value,
            'event_type': 'create'  # Thêm thông tin loại sự kiện
        }
        publish_message(topic, payload)

        return redirect('listdevice')

@login_required
def device_edit(request):
    if request.method == 'POST':
        device_id = request.POST.get('id')
        device = get_object_or_404(Device, id=device_id, user=request.user)

        old_api_key = device.api_key.api_key
        old_pin = device.pin

        device.name = request.POST.get('name')
        device.type = int(request.POST.get('type'))
        device.pin = request.POST.get('pin')
        device.unit = request.POST.get('unit')
        device.value = request.POST.get('value', '0')

        device.save()

        old_topic = f"API/{old_api_key}/{old_pin}/"
        client = connect_mqtt()
        if client:
            client.publish(old_topic, payload=None, retain=False)
            client.loop_start()

        new_api_key = device.api_key.api_key
        new_pin = device.pin
        new_topic = f"API/{new_api_key}/{new_pin}/"
        payload = {
            'value': device.value,
            'event_type': 'create'  # Thêm thông tin loại sự kiện
        }
        publish_message(new_topic, payload)
        client.loop_stop()

        return redirect('listdevice')

    return redirect('listdevice')
    
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
