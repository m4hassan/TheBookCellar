# Generated by Django 4.1 on 2024-11-07 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='product',
            name='is_sales',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='sales_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
