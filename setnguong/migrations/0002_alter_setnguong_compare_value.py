# Generated by Django 4.2.2 on 2024-05-25 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setnguong', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setnguong',
            name='compare_value',
            field=models.CharField(help_text='PIN value from V0 to V50', max_length=3),
        ),
    ]