from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse
from datas.models import Data
from devices.models import Device 
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
def update_value(request, api_key, pin):

    api_key = str(api_key)
    pin = str(pin)
    try:
        device = get_object_or_404(Device, api_key__api_key=api_key, pin=pin)
        device.value = request.GET.get('value')
        device.save()
      
        sensors = Device.objects.filter(type=2)
        relays = Device.objects.filter(type=1)
        if device.type ==2:
            data = Data.objects.create(api_key=api_key, pin=pin, name=device.name, value=device.value, date=timezone.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',  
            {
                'type': 'send_notification',
                'message': "ghiihihih" 
            }
        )
        return HttpResponse("ok")
    except Http404:

        return HttpResponse("Device not found.", status=404)
def get_value(request, api_key, pin):

    api_key = str(api_key)
    pin = str(pin)
    try:

        device = get_object_or_404(Device, pin=pin, api_key__api_key=api_key)

        return HttpResponse(device.value)
    except Http404:

        return HttpResponse("Device not found.", status=404)
    
