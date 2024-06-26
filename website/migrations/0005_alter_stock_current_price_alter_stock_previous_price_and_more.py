# Generated by Django 4.2.13 on 2024-06-04 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_remove_stock_owner_remove_stock_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='current_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stock',
            name='previous_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
