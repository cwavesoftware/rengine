# Generated by Django 3.2.4 on 2022-04-27 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanEngine', '0011_hackerone'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='notif_threshold',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]