
import os
import threading
import time
from django.shortcuts import get_object_or_404
from django.utils import timezone
import requests
from auto.models import Auto
from hengio.models import Hengio
from time import sleep
from devices.models import Device
from datas.models import Data
import socket

def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def check_hengio_tasks():

    today = timezone.datetime.now()
    current_time = today.time()
    current_day = today.weekday()  

    hengios = Hengio.objects.all()
    for hengio in hengios:
        days_of_week_nums = [int(day) for day in hengio.days_of_week]
        if current_day in days_of_week_nums and hengio.time.hour == current_time.hour and hengio.time.minute == current_time.minute:
            print(f"Thông báo: Thiết bị '{hengio.name}' cần được kích hoạt.")
            device = get_object_or_404(Device, api_key__api_key=hengio.api_key, pin=hengio.pin)
            device.value = hengio.status
            device.save()
def auto_van_task():
    autos = Auto.objects.filter(auto_status=Auto.ON)
    if not autos.exists():
      #  print("Không tìm thấy thiết bị với trạng thái ON. Thoát khỏi nhiệm vụ.")
        return

    ip = get_local_ip()
    relay_van = Device.objects.get(pin='V3')
    if relay_van.value =='1':
        sleep(5) 
        control_device( relay_van.api_key, relay_van.pin, Auto.OFF)
     #       print(f"Controlled van: {auto.van_pin} with status: {auto.van_status}")


      #  print(f"Địa chỉ IP cục bộ: {ip}")


def check_auto_tasks():
    autos = Auto.objects.filter(auto_status=Auto.ON)
    if not autos.exists():
        print("No devices with auto_status ON found. Exiting task.")
        return

    ip = get_local_ip()
   # print(f"Local IP: {ip}")

    for auto in autos:
        print(f"Processing auto: {auto.auto_name}")

        # Control pump
        if auto.pump_choice == Auto.CONTINUOUS:
            control_device(auto.api_key, auto.pump_pin, Auto.ON)
          
        # Control van
        sensor_water = Device.objects.get(pin='V6')
        
        if sensor_water.value=='1.00':
            if auto.van_status == Auto.ON:
                control_device( auto.api_key, auto.van_pin, Auto.ON)
     #       print(f"Controlled van: {auto.van_pin} with status: {auto.van_status}")

       #     print(f"Controlled van: {auto.van_pin} with status: {Auto.OFF}")
        # Control pH
        sensors_ph = Device.objects.filter(pin='V5')
        if sensors_ph.exists():
            sensor_ph_value = float(sensors_ph.first().value)
            min_ph = float(auto.min_ph)
            max_ph = float(auto.max_ph)
         #   print(f"Sensor pH value: {sensor_ph_value}, Min pH: {min_ph}, Max pH: {max_ph}")
            device = Device.objects.get(pin='V1')
         #   print(device.value)
            if ( min_ph > sensor_ph_value or max_ph < sensor_ph_value) and  device.value =='0':
                control_device( auto.api_key, auto.ph_pin, Auto.ON)
              #  print(f"Controlled pH: {auto.ph_pin} with status: {Auto.ON}")
            elif min_ph < sensor_ph_value and max_ph > sensor_ph_value and device.value =='1':
                control_device( auto.api_key, auto.ph_pin, Auto.OFF)
               # print(f"Controlled pH: {auto.ph_pin} with status: {Auto.OFF}")
        else:
            print("No pH sensor found with pin V5")

        # Control light
        sensors_light = Device.objects.filter(pin='V4')
        if sensors_light.exists():
            sensor_light_value = float(sensors_light.first().value)
            min_light = float(auto.min_light)
            print(f"Sensor light value: {sensor_light_value}, Min light: {min_light}")
            device = Device.objects.get(pin='V2')
            print(device.value)
            if sensor_light_value < min_light and device.value == '0':
                control_device(auto.api_key, auto.light_pin, Auto.ON)
        #        print(f"Controlled light: {auto.light_pin} with status: {Auto.ON}")
            elif sensor_light_value > min_light and device.value == '1':
                control_device( auto.api_key, auto.light_pin, Auto.OFF)
           #     print(f"Controlled light: {auto.light_pin} with status: {Auto.OFF}")
        else:
            print("No light sensor found with pin V4")
def auto_pump_task():
    autos = Auto.objects.filter(auto_status=Auto.ON)
    if not autos.exists():
        print("Không tìm thấy thiết bị với trạng thái ON. Thoát khỏi nhiệm vụ.")
        return

    ip = get_local_ip()
      #  print(f"Địa chỉ IP cục bộ: {ip}")

    for auto in autos:

        print(f"Xử lý thiết bị: {auto.auto_name}")

        if auto.pump_choice == Auto.INTERVAL:
            relay_van = Device.objects.get(pin='V0')
            if relay_van.value =="0":
                control_device( auto.api_key, auto.pump_pin, Auto.ON)
            else:
                control_device( auto.api_key, auto.pump_pin, Auto.OFF)
        else:
            print("Phát hiện tùy chọn không phải là INTERVAL. Kết thúc nhiệm vụ.")
        return
def control_device(api_key, pin, value):

    device_ip = os.environ.get('HOST', '')

    if not device_ip:
        print("Không tìm thấy giá trị HOST trong biến môi trường hoặc biến môi trường chưa được đặt.")
        return False

    url = f'http://{device_ip}/update/{api_key}/{pin}/?value={value}'
    print(url)
    response = requests.get(url)
    return response.status_code == 200