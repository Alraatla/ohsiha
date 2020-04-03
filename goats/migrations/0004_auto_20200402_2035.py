# Generated by Django 3.0.3 on 2020-04-02 17:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goats', '0003_auto_20200402_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goat',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
