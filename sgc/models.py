from platform import processor
from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField


def generate_matricula():
    return str(uuid4())

# Criação de um UserManager personalizado para o modelo Usuario


class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser):
    id = models.BigAutoField(
        primary_key=True, unique=True, auto_created=True, null=False)
    matricula = models.UUIDField(
        default=generate_matricula, unique=True, editable=False)
    data_criacao = models.DateTimeField(auto_now_add=True, null=True)
    data_alteracao = models.DateTimeField(auto_now=True, null=True)
    nome = models.CharField(max_length=50, null=False)
    email = models.EmailField(unique=True, null=False)
    sobrenome = models.CharField(max_length=70, null=False)
    tipo_acesso = models.ForeignKey(
        "TipoAcesso", on_delete=models.PROTECT, null=True)

    # Campos obrigatórios para AbstractBaseUser
    is_active = models.BooleanField(default=True, null=True)
    is_staff = models.BooleanField(default=False, null=True)

    # Configuração do gerenciador de usuários personalizado
    objects = UsuarioManager()

    # Campo para autenticação (substitui o username)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'sobrenome']

    def __str__(self):
        return f"{self.nome} {self.sobrenome} - {self.email}"

    # Métodos necessários para AbstractBaseUser
    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff


class TipoAcesso(models.Model):
    ALUNO = 'aluno'
    PROFESSOR = 'professor'
    COORDENADOR = 'cordenador'
    TIPOS_ACESSO_CHOICES = [
        (ALUNO, 'aluno'),
        (PROFESSOR, 'professor'),
        (COORDENADOR, 'coordenador'),
    ]
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(
        max_length=50, unique=True, null=False)
    descricao = models.TextField(blank=True, null=False)

    def __str__(self):
        return self.nome


class Professor(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, to_field='matricula', unique=True, related_name='professor', null=False)
    formacao = models.CharField(max_length=100, null=False)
    area_atuacao = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"{self.usuario.nome} {self.usuario.sobrenome} - Professor"


class Aluno(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, to_field='matricula', unique=True, related_name='aluno', null=False)
    curso = models.CharField(max_length=100, null=False)
    turma = models.CharField(max_length=20, null=False)

    def __str__(self):
        return f"{self.usuario.nome} {self.usuario.sobrenome} - {self.matricula}"


class Coordenador(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, to_field='matricula', unique=True, related_name='coordenador', null=False)
    professores = models.ManyToManyField(Professor, related_name='professores')

    def __str__(self):
        return f"{self.usuario.nome} {self.usuario.sobrenome} - Coordenador"


class Post(models.Model):
    titulo = models.CharField(max_length=50)
    sumario = models.CharField(max_length=100)
    texto = models.TextField(max_length=255)
    autor = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, to_field='matricula', related_name="autor_id", null=False)
    criado_em = models.DateTimeField(
        auto_now_add=True, editable=False, null=False, blank=False)
    editado_em = models.DateTimeField(
        auto_now=True, editable=True, null=True, blank=False)

    def __str__(self):
        return self.titulo


# class Turma(models.Model):
#     nome = models.CharField(max_length=50, unique=True)
#     descricao = models.TextField(blank=True)
#     professor = models.ForeignKey(Professor, to_field='matricula', on_delete=models.PROTECT, related_name='turmas')  # Professor responsável
#     alunos = models.ManyToManyField(Aluno, related_name='turmas')
    # Implementação futura (data, horário e sala)

    # def __str__(self):
    #     return self.nome

# from django.db import models
# from .models import Usuario, Professor

# class Prova(models.Model):
#     titulo = models.CharField(max_length=100)
#     descricao = models.TextField()
#     professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
#     data_criacao = models.DateTimeField(auto_now_add=True)
#     data_limite = models.DateTimeField()

#     def __str__(self):
#         return self.titulo

# class Questao(models.Model):
#     prova = models.ForeignKey(Prova, on_delete=models.CASCADE, related_name='questoes')
#     enunciado = models.TextField()
#     tipo = models.CharField(max_length=20, choices=[
#         ('multipla_escolha', 'Múltipla Escolha'),
#         ('dissertativa', 'Dissertativa'),
#     ])
#     # Outros campos para opções de múltipla escolha (se necessário)

#     def __str__(self):
#         return self.enunciado[:50]  # Exibe os primeiros 50 caracteres do enunciado

# class Atividade(models.Model):
#     titulo = models.CharField(max_length=100)
#     descricao = models.TextField()
#     professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
#     data_criacao = models.DateTimeField(auto_now_add=True)
#     data_limite = models.DateTimeField()

#     def __str__(self):
#         return self.titulo

# class Resposta(models.Model):
#     questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
#     aluno = models.ForeignKey(Usuario, on_delete=models.CASCADE)
#     resposta_texto = models.TextField(blank=True, null=True)  # Para questões dissertativas
#     # Outros campos para armazenar respostas de múltipla escolha (se necessário)

#     def __str__(self):
#         return f"Resposta de {self.aluno} para {self.questao}"
