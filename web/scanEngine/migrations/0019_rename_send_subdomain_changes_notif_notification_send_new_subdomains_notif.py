# Generated by Django 3.2.4 on 2024-08-28 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scanEngine', '0018_notification_absolute_threshold'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='send_subdomain_changes_notif',
            new_name='send_new_subdomains_notif',
        ),
    ]