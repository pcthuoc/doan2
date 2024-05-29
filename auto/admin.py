from django.contrib import admin
from .models import Auto

class AutoAdmin(admin.ModelAdmin):
    # Các trường sẽ hiển thị trong danh sách
    list_display = ('auto_name', 'api_key', 'pump_choice', 'van_status', 'ph_status', 'light_status')
    
    # Các trường có thể tìm kiếm
    search_fields = ('auto_name', 'api_key')
    
    # Các trường có thể lọc
    list_filter = ('pump_choice', 'van_status', 'ph_status', 'light_status')
    
    # Cấu hình chi tiết cho giao diện chỉnh sửa
    fieldsets = (
        (None, {
            'fields': ('api_key', 'auto_name','auto_status')
        }),
        ('Pump Configuration', {
            'fields': ('pump_choice', 'pump_pin')
        }),
        ('Valve Configuration', {
            'fields': ('van_status', 'van_pin')
        }),
        ('pH Configuration', {
            'fields': ('min_ph', 'max_ph', 'ph_status', 'ph_pin')
        }),
        ('Light Configuration', {
            'fields': ('min_light', 'light_status', 'light_pin')
        }),
    )

admin.site.register(Auto, AutoAdmin)
