# Generated by Django 4.1.4 on 2023-01-01 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_category_alter_listing_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bid',
            options={'ordering': ('-time_up',)},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('category',)},
        ),
        migrations.RemoveField(
            model_name='listing',
            name='terminate',
        ),
    ]
