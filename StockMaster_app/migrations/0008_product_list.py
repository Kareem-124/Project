# Generated by Django 4.2.11 on 2024-05-11 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StockMaster_app', '0007_rename_p_barcode_order_total_weight_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_name', models.CharField(max_length=255)),
                ('qty', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('total_weight', models.FloatField()),
                ('weight', models.FloatField()),
                ('products', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
