# Generated by Django 5.2.4 on 2025-07-22 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_remove_order_order_type_cartitem_item_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='discount_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='is_on_sale',
            field=models.BooleanField(default=False),
        ),
    ]
