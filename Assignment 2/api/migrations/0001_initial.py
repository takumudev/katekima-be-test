# Generated by Django 5.1.3 on 2025-04-13 15:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('unit', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('stock', models.IntegerField(default=0)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseHeader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('date', models.DateField()),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SellHeader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('date', models.DateField()),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('quantity', models.IntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('remaining_quantity', models.IntegerField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_details', to='api.item')),
                ('header', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='api.purchaseheader')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SellDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('quantity', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sell_details', to='api.item')),
                ('header', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='api.sellheader')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SellAllocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('quantity', models.IntegerField()),
                ('purchase_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocations', to='api.purchasedetail')),
                ('sell_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocations', to='api.selldetail')),
            ],
            options={
                'unique_together': {('sell_detail', 'purchase_detail')},
            },
        ),
    ]
