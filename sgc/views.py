from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, requires_csrf_token
from django.conf import settings
from gotrue.errors import AuthApiError
from sgc.models import TipoAcesso, Usuario, Professor

from .forms import CadastroForm, FormularioLogin


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
        form = CadastroForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.data['confirm_password']
            nome = form.cleaned_data['nome']
            sobrenome = form.cleaned_data['sobrenome']
            # Pelo ID cadastrado
            tipo_acesso = form.cleaned_data['tipo_acesso'] # 1 professor; 2 - aluno; 

            # Obter configurações padrão
            _supabase = settings.SUPABASE

            # Cria o usuário no Supabase
            try:
                # _response = _supabase.auth.sign_up(
                #     {
                #         "email": email,
                #         "password": password,
                #     }
                # )
                usuario = Usuario.objects.create(
                    nome=nome,
                    sobrenome=sobrenome,
                    email=email,
                    tipo_acesso=tipo_acesso,
                )
                print("TESTE", tipo_acesso)
                if str(tipo_acesso) == "Professor":
                    Professor.objects.create(usuario=usuario, formacao='Ciência da Computação', area_atuacao='Python')
                # if usuario:
                #     # Usuário criado com sucesso, volta para o index
                #     messages.success(
                #         request, 'Usuário cadastrado com sucesso! Verifique seu e-mail para confirmar a conta.')
                #     return redirect(index)
                # # else:
                # #     # Usuário NÃO criado, volta para para a tela de cadastro
                # #     print("Erro ao criar usuario no Supabase")
                # #     messages.error(
                # #         request, 'Erro ao cadastrar o usuário. Tente novamente mais tarde')
                #     return redirect(cadastrar_usuario_view)
            except AuthApiError as e:
                messages.error(
                    request, f"Erro na API de autenticação do Supabase: {e}")
            except Exception as e:
                print("Erro ao criar usuario no Supabase", e)
                messages.error(request, f"Erro inesperado: {e}")
            return render(request, 'sgc/cadastro_usuario.html', {'form': form})
    else:
        form = CadastroForm()
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
                        # Sessão expira quando o navegador é fechado
                        request.session.set_expiry(0)
                    return redirect(index)
                # else:
                #     pass
                #     messages.error(request, f"Erro ao fazer login com usuario. Verifique se você ja fez login.")
                #     return redirect(login_view)
            except Exception:
                messages.error(request, f"Erro do ao entrar como {
                               email}: {user}")
                return redirect(login_view)
    else:
        form = FormularioLogin()
    return render(request, 'sgc/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(index)  # Redireciona para a página de login
