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
        value = request.GET.get('value')
        
        if value:
            device.value = value
            device.save()
            
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                    'updates',  
                    {
                        'type': 'send_update',
                        'pin': device.pin,
                        'value': device.value
                    }
                )

            return HttpResponse("ok")
        else:
            return HttpResponse("No value provided.", status=400)
    except Http404:
        return HttpResponse("Device not found.", status=404)
    

def update_sensor(request, api_key, pin):
    api_key = str(api_key)
    pin = str(pin)
    
    try:
        device = get_object_or_404(Device, api_key__api_key=api_key, pin=pin)
        value = request.GET.get('value')
        
        if value:
            current_time = timezone.datetime.now()
            last_update = Data.objects.filter(api_key=api_key, pin=pin).order_by('-date').first()
            if not last_update or (current_time - last_update.date).total_seconds() >= 60:
                device.value = value
                device.save()
                Data.objects.create(api_key=api_key, pin=pin, name=device.name, value=device.value,  date=timezone.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'notifications',  
                    {
                        'type': 'send_notification',
                        'message': "ghihihih"
                    }
                )
                return HttpResponse("ok")
            else:
                return HttpResponse("Value updated less than a minute ago.", status=429) 
        else:
            return HttpResponse("No value provided.", status=400)
    except Http404:
        return HttpResponse("Device not found.", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
    

def update_multi(request):
    if request.method == 'GET':
        try:
            query_params = request.GET.dict()
            pin_value_pairs = [(key, value) for key, value in query_params.items() if key.startswith('V')]
            for pin, value in pin_value_pairs:
                device = get_object_or_404(Device, pin=pin)
                device.value = value
                device.save()
                Data.objects.create(api_key=device.api_key.api_key, pin=pin, name=device.name, value=value,date=timezone.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                    'notifications',  
                    {
                        'type': 'send_notification',
                        'message': "ghihihih" 
                    }
                )
       
            return JsonResponse({'message': 'ok'})
        except Exception as e:
   
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
def get_value(request, api_key, pin):
    api_key = str(api_key)
    pin = str(pin)
    try:
        device = get_object_or_404(Device, pin=pin, api_key__api_key=api_key)
        return HttpResponse(device.value)
    except Http404:
        return HttpResponse("Device not found.", status=404)

def get_all_values(request):
    try:
        # Lấy tất cả các thiết bị từ V0 đến V3
        devices = Device.objects.filter(type=1).values('pin', 'value')
        
        # Tạo một dictionary để lưu trữ giá trị của các thiết bị
        values = {device['pin']: device['value'] for device in devices}
        return JsonResponse(values)
    except Exception as e:
        # Xử lý các trường hợp ngoại lệ
        return JsonResponse({'error': str(e)}, status=500)
