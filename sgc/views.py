from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, requires_csrf_token
from django.conf import settings
from gotrue.errors import AuthApiError

from .forms import FormularioCadastrarUsuario, FormularioLogin


def index(request):
    # Verifica se o usuário está autenticado
    if request.user.is_authenticated:
        # Se estiver autenticado, obtém o nome do usuário do Supabase (você precisará implementar essa lógica)
        # Substitua 'nome' pelo atributo correto no seu modelo de usuário
        nome_usuario = request.user.email
    else:
        nome_usuario = None  # Ou defina um valor padrão, como "Visitante"
    # Renderiza o template index.html, passando o nome do usuário no contexto
    return render(request, 'sgc/index.html', {'user': request.user, 'username': nome_usuario})

@requires_csrf_token
@csrf_protect
def cadastrar_usuario_view(request):
    if request.method == 'POST':
        form = FormularioCadastrarUsuario(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Obter configurações padrão
            _supabase = settings.SUPABASE

            # Cria o usuário no Supabase
            try:
                _response = _supabase.auth.sign_up(
                    {
                        "email": email,
                        "password": password,
                    }
                )

                if _response:
                    # Usuário criado com sucesso, volta para o index
                    messages.success(
                        request, 'Usuário cadastrado com sucesso! Verifique seu e-mail para confirmar a conta.')
                    return redirect(index)
                else:
                    # Usuário NÃO criado, volta para para a tela de cadastro
                    print("Erro ao criar usuario no Supabase")
                    messages.error(
                        request, 'Erro ao cadastrar o usuário. Tente novamente mais tarde')
                    return redirect(cadastrar_usuario_view)
            except Exception as e:
                print("Erro ao criar usuario no Supabase")
                messages.error(request, f"Erro inesperado: {e}")
                return render(request, 'sgc/cadastro_usuario.html', {'form': form})

    else:
        form = FormularioCadastrarUsuario()
    return render(request, 'sgc/cadastro_usuario.html', {'form': form})


@requires_csrf_token
@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = FormularioLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            lembrar_de_mim = form.data.get('remember_me') == 'on'

            try:
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    if lembrar_de_mim:
                        request.session.set_expiry(1209600)  # 2 semanas
                    else:
                        request.session.set_expiry(0)  # Sessão expira quando o navegador é fechado
                    return redirect(index)
                # else:
                #     pass
                #     messages.error(request, f"Erro ao fazer login com usuario. Verifique se você ja fez login.")
                #     return redirect(login_view)
            except Exception:
                messages.error(request, f"Erro do ao entrar como {email}: {user}")
                return redirect(login_view)
    else:
        form = FormularioLogin()
    return render(request, 'sgc/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(index)  # Redireciona para a página de login
