# Generated by Django 5.0.6 on 2024-06-03 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgc', '0010_alter_post_sumario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='sumario',
            field=models.CharField(max_length=100),
        ),
    ]
