# Generated by Django 4.2.11 on 2024-05-12 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StockMaster_app', '0008_product_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='p_price',
        ),
        migrations.AddField(
            model_name='order',
            name='p_name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
