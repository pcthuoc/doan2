from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminTimeWidget

from setnguong.models import Setnguong
# Register your models here.
class SetNguongForm(forms.ModelForm):
    time = forms.TimeField(widget=AdminTimeWidget(format='%H:%M'))

    class Meta:
        model = Setnguong
        fields = '__all__'
@admin.register(Setnguong)
class HengioAdmin(admin.ModelAdmin):
    form = SetNguongForm
    list_display = ('sensor_name', 'relay_name', 'compare', 'compare_value','status')
    list_filter = ('sensor_name', 'relay_name', 'compare', 'compare_value','status')
    search_fields = ('sensor_name', 'relay_name', 'compare', 'compare_value','status')
