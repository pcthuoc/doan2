# Generated by Django 4.2.2 on 2024-05-25 13:38

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
                ('status', models.CharField(default='0', help_text='Value of the sensor', max_length=20)),
                ('value', models.IntegerField(choices=[(1, 'On'), (2, 'Off')], default=1, help_text='Type')),
                ('time', models.TimeField(help_text='Time to trigger the event')),
                ('days_of_week', multiselectfield.db.fields.MultiSelectField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], default=[0, 1, 2, 3, 4, 5, 6], help_text='Days of the week when the event should trigger', max_length=7)),
            ],
            options={
                'verbose_name_plural': 'Hengios',
            },
        ),
    ]
