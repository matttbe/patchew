# Generated by Django 3.1.14 on 2022-09-19 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0067_result_denormalize'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='project_denorm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='api.project'),
        ),
    ]