# Generated by Django 4.2.13 on 2024-05-26 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setnguong', '0004_alter_setnguong_days_of_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='setnguong',
            name='status',
            field=models.IntegerField(choices=[(1, 'On'), (2, 'Off')], default=1, help_text='Type'),
        ),
    ]