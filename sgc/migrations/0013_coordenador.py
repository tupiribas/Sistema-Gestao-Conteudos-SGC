# Generated by Django 5.0.6 on 2024-06-03 06:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgc', '0012_post_editado_em_alter_post_criado_em'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coordenador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('professores', models.ManyToManyField(related_name='professores', to='sgc.professor')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='coordenador', to='sgc.usuario', to_field='matricula')),
            ],
        ),
    ]
