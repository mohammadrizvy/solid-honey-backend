# Generated by Django 4.2 on 2024-09-24 03:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shss', '0007_my_check_out_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Web_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='my_check_out',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shss.saleing_product'),
        ),
        migrations.CreateModel(
            name='Stock_Saleing_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('qt', models.PositiveIntegerField()),
                ('sp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shss.saleing_product')),
            ],
        ),
        migrations.AlterField(
            model_name='saleing_product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shss.web_category'),
        ),
    ]
