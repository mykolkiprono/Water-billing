# Generated by Django 4.1.7 on 2023-04-21 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0010_alter_waterbill_client'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='plan',
        ),
    ]