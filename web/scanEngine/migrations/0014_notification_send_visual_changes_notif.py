# Generated by Django 3.2.4 on 2022-05-16 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanEngine', '0013_notification_send_removed_subdomains_notif'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='send_visual_changes_notif',
            field=models.BooleanField(default=True),
        ),
    ]