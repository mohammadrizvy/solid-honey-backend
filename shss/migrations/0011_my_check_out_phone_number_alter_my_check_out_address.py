# Generated by Django 4.2 on 2024-09-28 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shss', '0010_saleing_product_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='my_check_out',
            name='phone_number',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='my_check_out',
            name='address',
            field=models.TextField(max_length=500),
        ),
    ]
