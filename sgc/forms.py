from django import forms
from django import forms
from .models import Usuario, TipoAcesso


class CadastroForm(forms.ModelForm):
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


class FormularioLogin(forms.Form):
    email = forms.EmailField(label='E-mail', required=True)
    password = forms.CharField(
        label='Senha', widget=forms.PasswordInput, required=True)
    lembrar_de_mim = forms.BooleanField(label='Lembrar de mim', widget=forms.CheckboxInput(
        attrs={'class': 'lembrar-de-mim'}), required=False)
