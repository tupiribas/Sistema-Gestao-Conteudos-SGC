# Generated by Django 5.0.6 on 2024-06-03 00:32

import ckeditor.fields
import ckeditor_uploader.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgc', '0007_aluno'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('sumario', ckeditor.fields.RichTextField()),
                ('texto', ckeditor_uploader.fields.RichTextUploadingField()),
                ('criado_em', models.DateField(auto_now=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sgc.usuario', to_field='matricula')),
            ],
        ),
    ]
