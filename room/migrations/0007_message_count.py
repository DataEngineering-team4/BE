# Generated by Django 4.2.1 on 2023-05-25 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0006_alter_message_options_alter_room_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='count',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]