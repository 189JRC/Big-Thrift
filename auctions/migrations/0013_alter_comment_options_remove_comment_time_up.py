# Generated by Django 4.1.4 on 2023-01-02 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_comment_options_comment_time_up_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={},
        ),
        migrations.RemoveField(
            model_name='comment',
            name='time_up',
        ),
    ]
