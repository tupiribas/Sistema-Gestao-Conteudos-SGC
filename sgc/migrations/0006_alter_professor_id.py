# Generated by Django 5.0.3 on 2024-05-26 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgc', '0005_alter_professor_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]