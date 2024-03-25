# Generated by Django 4.2.5 on 2024-03-13 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapi', '0008_remove_report_damage_cost_report_customer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'cash'), ('online', 'online')], default='online', max_length=50),
        ),
        migrations.AlterField(
            model_name='vehiclepurchase',
            name='purchase_method',
            field=models.CharField(choices=[('cash', 'cash'), ('online', 'online')], default='online', max_length=50),
        ),
        migrations.AlterField(
            model_name='vehiclepurchase',
            name='purchase_status',
            field=models.CharField(choices=[('pending', 'pending'), ('processing', 'processing'), ('failed', 'failed'), ('completed', 'completed')], default='completed', max_length=50),
        ),
    ]