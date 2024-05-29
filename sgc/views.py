from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, requires_csrf_token
from django.contrib.auth.decorators import login_required
from django.conf import settings
from gotrue.errors import AuthApiError
from sgc.models import TipoAcesso, Usuario, Professor, Aluno

from .forms import AlunoForm, CadastrarAlunoForm, CadastrarProfessorForm, CadastroUsuarioForm, LoginForm, ProfessorForm, UsuarioForm


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
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            tipo_acesso = form.cleaned_data['tipo_acesso']
            tipo_acesso_obj = TipoAcesso.objects.get(nome=str(tipo_acesso))
            request.session['cadastro_data'] = form.data
            if tipo_acesso_obj.nome == "Aluno":
                return redirect(reverse('processar_cadastro_aluno_view'))
            elif tipo_acesso_obj.nome == "Professor":
                return redirect(reverse('processar_cadastro_professor_view'))
    else:
        form = CadastroUsuarioForm()
    return render(request, 'sgc/cadastro_usuario.html', {'form': form})


@requires_csrf_token
@csrf_protect
def processar_cadastro_aluno_view(request):
    if request.method == 'POST':
        form = CadastrarAlunoForm(request.POST)
        if form.is_valid():
            cadastro_data = request.session.get('cadastro_data', {})
            nome = cadastro_data.get('nome')
            sobrenome = cadastro_data.get('sobrenome')
            email = cadastro_data.get('email')
            password = cadastro_data.get('password')
            tipo_acesso = int(cadastro_data.get('tipo_acesso'))
            curso = form.cleaned_data['curso']
            turma = form.cleaned_data['turma']

            # Obter configurações padrão
            _supabase = settings.SUPABASE
            # Cadastrar authenticação
            _response = _supabase.auth.sign_up(
                {
                    "email": email,
                    "password": password, }
            )

            # Salve o usuário e o aluno no banco de dados
            _usuario = Usuario.objects.create(
                nome=nome, sobrenome=sobrenome, email=email, tipo_acesso=TipoAcesso.objects.get(
                    id=tipo_acesso)
            )
            _aluno = Aluno.objects.create(
                usuario=_usuario, curso=curso, turma=turma)
            messages.success(
                request, 'Cadastro de aluno realizado com sucesso!')
            del request.session['cadastro_data']
            return redirect('login')
    else:
        form = CadastrarAlunoForm()
    return render(request, 'sgc/cadastro_aluno.html', {'form': form})


@requires_csrf_token
@csrf_protect
def processar_cadastro_professor_view(request):
    if request.method == 'POST':
        form = CadastrarProfessorForm(request.POST)
        if form.is_valid():
            cadastro_data = request.session.get('cadastro_data', {})
            # print(cadastro_data)
            nome = cadastro_data.get('nome')
            sobrenome = cadastro_data.get('sobrenome')
            email = cadastro_data.get('email')
            password = cadastro_data.get('password')
            tipo_acesso = int(cadastro_data.get('tipo_acesso'))
            formacao = form.cleaned_data['formacao']
            area_atuacao = form.cleaned_data['area_atuacao']

            # Obter configurações padrão
            _supabase = settings.SUPABASE
            # Cadastrar authenticação
            _response = _supabase.auth.sign_up(
                {
                    "email": email,
                    "password": password, }
            )

            # Salvando o usuário e o professor no banco de dados
            _usuario = Usuario.objects.create(
                nome=nome, sobrenome=sobrenome, email=email, tipo_acesso=TipoAcesso.objects.get(
                    id=tipo_acesso)
            )
            _professor = Professor.objects.create(
                usuario=_usuario, formacao=formacao, area_atuacao=area_atuacao)
            messages.success(
                request, 'Cadastro de professor realizado com sucesso!')
            del request.session['cadastro_data']
            return redirect('login')
    else:
        form = CadastrarProfessorForm()
    return render(request, 'sgc/cadastro_professor.html', {'form': form})


@requires_csrf_token
@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
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
                else:
                    messages.error(
                        request, f"Erro ao fazer login com usuario. Verifique se você ja fez login.")
                    return redirect(login_view)
            except Exception:
                messages.error(request, f"Erro do ao entrar como {
                               email}: {user}")
                return redirect(login_view)
    else:
        form = LoginForm()
    return render(request, 'sgc/login.html', {'form': form})


@login_required(login_url='/login')
def perfil_view(request):
    try:
        user = Usuario.objects.get(email=request.user.email)
        if str(user.tipo_acesso) == "Professor":
            perfil = Professor.objects.get()
            form_class = ProfessorForm
        elif str(user.tipo_acesso) == "Aluno":
            perfil = Aluno.objects.get()
            form_class = AlunoForm
        else:
            perfil = user
            form_class = UsuarioForm
    except Usuario.DoesNotExist as e:
        print("Usuário não existe!", e)
        messages.error(request, 'Usuário não existe!')

    if request.method == 'POST':
        form = form_class(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            # Redireciona para a mesma página após a atualização
            return redirect(perfil_view)
        else:
            form = form_class(instance=perfil)

    return render(request, 'sgc/perfil.html', {'form': form_class, 'perfil': perfil, 'usuario': user})


def logout_view(request):
    logout(request)
    return redirect(index)  # Redireciona para a página de login
