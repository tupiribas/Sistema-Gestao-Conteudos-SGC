# Generated by Django 5.0.3 on 2024-05-23 03:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgc', '0003_aluno'),
    ]

    operations = [
        migrations.CreateModel(
            name='Atividade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_limite', models.DateTimeField()),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sgc.professor')),
            ],
        ),
        migrations.CreateModel(
            name='Prova',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_limite', models.DateTimeField()),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sgc.professor')),
            ],
        ),
        migrations.CreateModel(
            name='Questao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enunciado', models.TextField()),
                ('tipo', models.CharField(choices=[('multipla_escolha', 'Múltipla Escolha'), ('dissertativa', 'Dissertativa')], max_length=20)),
                ('prova', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questoes', to='sgc.prova')),
            ],
        ),
        migrations.CreateModel(
            name='Resposta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resposta_texto', models.TextField(blank=True, null=True)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sgc.usuario')),
                ('questao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sgc.questao')),
            ],
        ),
    ]