# Generated by Django 4.2.13 on 2024-09-08 16:27

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hengio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.CharField(help_text='Device API Key', max_length=30)),
                ('pin', models.CharField(help_text='PIN value from V0 to V50', max_length=3)),
                ('name', models.CharField(help_text='Device name', max_length=30)),
                ('status', models.IntegerField(choices=[(1, 'On'), (2, 'Off')], default=1, help_text='Value of the sensor')),
                ('value', models.IntegerField(choices=[(1, 'On'), (2, 'Off')], default=1, help_text='Type')),
                ('time', models.TimeField(help_text='Time to trigger the event')),
                ('days_of_week', multiselectfield.db.fields.MultiSelectField(choices=[(0, 'Hai'), (1, 'Ba'), (2, 'Tư'), (3, 'Năm'), (4, 'Sáu'), (5, 'Bảy'), (6, 'Chủ Nhật')], default=[0, 1, 2, 3, 4, 5, 6], help_text='Days of the week when the event should trigger', max_length=13)),
            ],
            options={
                'verbose_name_plural': 'Hengios',
            },
        ),
    ]
