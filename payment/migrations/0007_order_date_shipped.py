# Generated by Django 4.1 on 2024-12-02 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_order_shipped_alter_order_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date_shipped',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
