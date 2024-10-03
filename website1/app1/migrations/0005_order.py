# Generated by Django 5.0.6 on 2024-07-27 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_user', models.CharField(default=None, max_length=250)),
                ('order_name', models.CharField(max_length=250)),
                ('order_price', models.CharField(max_length=250)),
                ('order_image', models.CharField(max_length=250, null=True)),
                ('order_qty', models.IntegerField()),
                ('order_amount', models.IntegerField()),
                ('order_address', models.TextField(null=True)),
                ('order_dlvtype', models.CharField(max_length=10, null=True)),
                ('order_status', models.IntegerField(default=0)),
            ],
        ),
    ]
