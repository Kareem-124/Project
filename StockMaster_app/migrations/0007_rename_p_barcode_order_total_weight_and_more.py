# Generated by Django 4.2.11 on 2024-05-11 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StockMaster_app', '0006_remove_order_weight_alter_order_p_barcode_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='p_barcode',
            new_name='total_weight',
        ),
        migrations.RenameField(
            model_name='order_list',
            old_name='p_barcode',
            new_name='total_weight',
        ),
        migrations.RenameField(
            model_name='prodcut',
            old_name='expire_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='prodcut',
            old_name='cost',
            new_name='total_weight',
        ),
        migrations.RenameField(
            model_name='prodcut',
            old_name='p_barcode',
            new_name='weight',
        ),
    ]
