from django import forms


class FormularioCadastrarUsuario(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)  # Opcional


class FormularioLogin(forms.Form):
    email = forms.EmailField(label='E-mail', required=True)
    password = forms.CharField(
        label='Senha', widget=forms.PasswordInput, required=True)
    lembrar_de_mim = forms.BooleanField(label='Lembrar de mim', required=False)
