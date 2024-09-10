from django.contrib import admin
from .models import Hengio
from django import forms
from django.contrib.admin.widgets import AdminTimeWidget

class HengioForm(forms.ModelForm):
    time = forms.TimeField(widget=AdminTimeWidget(format='%H:%M'))

    class Meta:
        model = Hengio
        fields = '__all__'

@admin.register(Hengio)
class HengioAdmin(admin.ModelAdmin):
    form = HengioForm
    list_display = ('pk', 'name', 'status', 'time', 'days_of_week')
    list_filter = ('name', 'status', 'days_of_week')
    search_fields = ('name', 'api_key', 'pin')
