# Generated by Django 4.2 on 2024-09-03 07:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.CharField(max_length=15)),
                ('product_name', models.CharField(max_length=255)),
                ('unitperreceipt', models.FloatField()),
                ('buying_price', models.FloatField()),
                ('saleing_price', models.FloatField()),
                ('wholesale_price', models.FloatField()),
                ('alart', models.FloatField()),
                ('discount', models.FloatField()),
                ('img', models.ImageField(upload_to='media/products/')),
                ('point', models.FloatField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shpos.category')),
                ('entry_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shpos.unit')),
            ],
        ),
    ]
