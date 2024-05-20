from django.db import models
from uuid import uuid4


class Usuario(models.Model):
    data_criacao = models.DateTimeField(auto_now=False, auto_now_add=True)
    data_alteracao = models.DateTimeField(auto_now=True, auto_now_add=False)
    nome = models.CharField(max_length=50, null=False)
    email = models.EmailField(unique=True, default='')
    sobrenome = models.CharField(max_length=70, null=False)

    def __str__(self):
        return f"{self.nome} {self.sobrenome} - {self.email}"

def generate_matricula():
    return str(uuid4())

class Professor(models.Model):
    matricula = models.UUIDField(primary_key=True, default=generate_matricula, editable=False)
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=70)
    email = models.EmailField(unique=True)
    formacao = models.CharField(max_length=100)
    area_atuacao = models.CharField(max_length=100)
    titulacao = models.CharField(max_length=50, blank=True, null=True)
