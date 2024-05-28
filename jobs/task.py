
from django.shortcuts import get_object_or_404
from django.utils import timezone
from hengio.models import Hengio
from setnguong.models import Setnguong
from devices.models import Device
from datas.models import Data
def check_hengio_tasks():
    # Lấy ngày và giờ hiện tại từ Django timezone
    today = timezone.datetime.now()
    current_time = today.time()
    current_day = today.weekday()  # 0 = Monday, 1 = Tuesday, ..., 6 = Sunday

    # Lấy tất cả các đối tượng Hengio
    hengios = Hengio.objects.all()
    print(current_time)
    # Duyệt qua từng đối tượng và kiểm tra điều kiện
    for hengio in hengios:
        days_of_week_nums = [int(day) for day in hengio.days_of_week]
        if current_day in days_of_week_nums and hengio.time.hour == current_time.hour and hengio.time.minute == current_time.minute:
            print(f"Thông báo: Thiết bị '{hengio.name}' cần được kích hoạt.")
            device = get_object_or_404(Device, api_key__api_key=hengio.api_key, pin=hengio.pin)
            device.value = hengio.status
            device.save()
def check_nguong_tasks():
    # Lấy ngày và giờ hiện tại từ Django timezone
    today = timezone.datetime.now()
    current_time = today.time()
    current_day = today.weekday()  

    # Lấy tất cả các đối tượng Hengio
    nguongs = Setnguong.objects.all()
    print(current_time)
    # Duyệt qua từng đối tượng và kiểm tra điều kiện
    for nguong in nguongs:
        days_of_week_nums = [int(day) for day in nguong.days_of_week]
        if current_day in days_of_week_nums and hengio.time.hour == current_time.hour and hengio.time.minute == current_time.minute:
            print(f"Thông báo: Thiết bị '{hengio.name}' cần được kích hoạt.")
            device = get_object_or_404(Device, api_key__api_key=hengio.api_key, pin=hengio.pin)
            device.value = hengio.status
            device.save()

