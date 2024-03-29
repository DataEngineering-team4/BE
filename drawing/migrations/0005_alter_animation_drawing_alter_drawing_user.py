# Generated by Django 4.2.1 on 2023-05-25 06:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drawing', '0004_alter_drawing_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animation',
            name='drawing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='animations', to='drawing.drawing'),
        ),
        migrations.AlterField(
            model_name='drawing',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drawings', to=settings.AUTH_USER_MODEL),
        ),
    ]
