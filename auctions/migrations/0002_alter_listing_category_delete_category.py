# Generated by Django 4.1.4 on 2023-01-01 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('CLOTHING', 'Clothing'), ('TOYS', 'Toys'), ('BOOKS', 'Books'), ('OUTDOORS', 'Outdoors'), ('HOMEWARE', 'Homeware'), ('COOKING', 'Cooking'), ('ELECTRONICS', 'Electronics'), ('ARTS & CRAFTS', 'Arts & Crafts'), ('OTHER', 'Other')], default='Other', help_text='Please select a category', max_length=40),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]