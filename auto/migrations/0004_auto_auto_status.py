# Generated by Django 4.2.13 on 2024-05-29 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0003_alter_auto_api_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='auto',
            name='auto_status',
            field=models.IntegerField(choices=[(1, 'On'), (2, 'Off')], default=2, help_text='Type'),
        ),
    ]
