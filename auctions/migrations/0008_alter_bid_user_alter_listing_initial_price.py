# Generated by Django 4.1.4 on 2023-01-01 15:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listing_initial_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='initial_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
