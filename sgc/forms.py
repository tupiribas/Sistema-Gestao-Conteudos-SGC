from django import forms
from django import forms
from .models import Aluno, Post, Professor, Usuario, TipoAcesso


class CadastroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label="Confirmar Senha")

    class Meta:
        model = Usuario
        fields = ['nome', 'sobrenome', 'email', 'tipo_acesso']
        widgets = {
            'tipo_acesso': forms.Select(choices=TipoAcesso.TIPOS_ACESSO_CHOICES),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "As senhas não coincidem."
            )
        return cleaned_data


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        # Campos comuns a todos os usuários
        fields = ['nome', 'sobrenome', 'email']

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['formacao', 'area_atuacao']  # Campos específicos de professor

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['curso', 'turma']

class CadastrarProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['formacao', 'area_atuacao']


class CadastrarAlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['curso', 'turma']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'sumario', 'texto']

class PostFiltrarForm(forms.Form):
    titulo = forms.CharField(label='Título', required=False)
    sumario = forms.CharField(label='Sumário', required=False)
    criado_em_inicio = forms.DateField(label='Criado em (início)', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    criado_em_fim = forms.DateField(label='Criado em (fim)', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    editado_em_inicio = forms.DateField(label='Editado em (início)', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    editado_em_fim = forms.DateField(label='Editado em (fim)', required=False, widget=forms.DateInput(attrs={'type': 'date'}))


class LoginForm(forms.Form):
    email = forms.EmailField(label='E-mail', required=True)
    password = forms.CharField(
        label='Senha', widget=forms.PasswordInput, required=True)
    lembrar_de_mim = forms.BooleanField(label='Lembrar de mim', widget=forms.CheckboxInput(
        attrs={'class': 'lembrar-de-mim'}), required=False)
