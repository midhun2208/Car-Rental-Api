# Generated by Django 4.2.5 on 2024-02-21 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminapi', '0002_rentaltransactions_rentalvehicle_usedvehicle_report_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehiclePurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('purchase_date', models.DateField(auto_now_add=True)),
                ('purchase_method', models.CharField(choices=[('cash', 'cash'), ('online', 'online')], default='cash', max_length=50)),
                ('purchase_status', models.CharField(choices=[('pending', 'pending'), ('processing', 'processing'), ('failed', 'failed'), ('completed', 'completed')], default='pending', max_length=50)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapi.usedvehicle')),
            ],
        ),
    ]