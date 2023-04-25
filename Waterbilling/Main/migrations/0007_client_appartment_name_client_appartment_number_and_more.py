# Generated by Django 4.1.7 on 2023-04-21 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0006_reportproblem_responseproblem_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='appartment_name',
            field=models.CharField(blank=True, default=None, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='appartment_number',
            field=models.CharField(blank=True, default=None, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='location',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='waterbill',
            name='status',
            field=models.TextField(choices=[('Paid', 'Paid'), ('overdue', 'overdue')], null=True),
        ),
    ]
