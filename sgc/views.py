from datetime import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, requires_csrf_token
from django.contrib.auth.decorators import login_required
from django.conf import settings
from gotrue.errors import AuthApiError
from sgc.models import (Coordenador, Post, TipoAcesso,
                        Usuario, Professor, Aluno)

from .forms import (AlunoForm, CadastrarAlunoForm, CadastrarProfessorForm, CadastroEscolaForm,
                    CadastroUsuarioForm, CoordenadorForm, LoginForm, PostFiltrarForm, PostForm, ProfessorForm, UsuarioForm)


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
            elif tipo_acesso_obj.nome == "Professor" or tipo_acesso_obj.nome == "Coordenador":
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
            tipo_acesso = cadastro_data.get('tipo_acesso')
            curso = form.cleaned_data['curso']
            turma = form.cleaned_data['turma']
            try:
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
                        id=int(tipo_acesso))
                )
                _aluno = Aluno.objects.create(
                    usuario=_usuario, curso=curso, turma=turma)
                messages.success(
                    request, 'Cadastro de aluno realizado com sucesso!')

                del request.session['cadastro_data']
                return redirect('login_view')
            except AuthApiError as e:
                print("Erro", e)
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
            print(tipo_acesso)
            try:
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
                if tipo_acesso == 2:
                    return redirect(reverse('processar_cadastro_coordenador_view'))
                else:
                    del request.session['cadastro_data']
                    return redirect(login_view)
            except AuthApiError as e:
                print("Erro:", e)
    else:
        form = CadastrarProfessorForm()
    return render(request, 'sgc/cadastro_professor.html', {'form': form})


@requires_csrf_token
@csrf_protect
def processar_cadastro_coordenador_view(request):
    if request.method == 'POST':
        form = CadastroEscolaForm(request.POST)
        if form.is_valid():
            cadastro_data = request.session.get('cadastro_data', {})
            email = cadastro_data.get('email')
            _supabase = settings.SUPABASE

            try:
                _usuario = Usuario.objects.get(email=email)
                try:
                    # Tente obter o Professor associado ao usuário
                    _professor = Professor.objects.get(usuario=_usuario)
                except Professor.DoesNotExist:
                    # Se o usuário não for um professor, redirecione para o cadastro de professor
                    messages.error(
                        request, 'Você precisa ser um professor para se cadastrar como coordenador.')
                    return redirect('processar_cadastro_professor_view')
                _coordenador = Coordenador.objects.create(
                    usuario=_usuario,
                )
                messages.success(
                    request, 'Coordenador cadastrado com sucesso!')
                # Adiciona o professor ao coordenador
                _coordenador.professores.add(_professor)
                print(_coordenador)
                del request.session['cadastro_data']
                return redirect(login_view)

            except AuthApiError as e:
                messages.error(
                    request, f"Erro na API de autenticação do Supabase: {e}")
            except Exception as e:
                messages.error(request, f"Erro inesperado: {e}")
    else:
        form = CadastroEscolaForm()
    return render(request, 'sgc/cadastro_coordenador.html', {'form': form})


@login_required(login_url='/login')
def perfil_view(request):
    try:
        user = Usuario.objects.get(email=request.user.email)
        if str(user.tipo_acesso) == "Professor":
            perfil = Professor.objects.get(usuario=user)
            form_class = ProfessorForm
        elif str(user.tipo_acesso) == "Aluno":
            perfil = Aluno.objects.get()
            form_class = AlunoForm
        elif str(user.tipo_acesso) == "Coordenador":
            perfil = user.coordenador
            form_class = CoordenadorForm
        else:
            perfil = user
            form_class = UsuarioForm
    except Usuario.DoesNotExist as e:
        print("Usuário não existe!", e)
        messages.error(request, 'Usuário não existe!')
        redirect(login)

    if request.method == 'POST':
        form = form_class(request.POST, instance=perfil)
        if form.is_valid():
            perfil = form.save()
            if str(user.tipo_acesso) == "Professor" or str(user.tipo_acesso) == "Coordenador":
                user.nome = perfil.usuario.nome
                user.sobrenome = perfil.usuario.sobrenome
                user.email = perfil.usuario.email
            user.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            # Redireciona para a mesma página após a atualização
            return redirect(perfil_view)
        else:
            form = form_class(instance=perfil)
    return render(request, 'sgc/perfil.html', {'form': form_class, 'perfil': perfil, 'usuario': user})


@login_required(login_url='/login')
@csrf_protect
def listar_posts_view(request):
    # Mostra toda a lista
    posts = Post.objects.all()
    # Filtrar as informações em conjunto e/ou individualmente e mostra na tela
    form = PostFiltrarForm(request.GET)
    if form.is_valid():
        titulo = form.cleaned_data['titulo']
        sumario = form.cleaned_data['sumario']
        criado_em_inicio = form.cleaned_data['criado_em_inicio']
        criado_em_fim = form.cleaned_data['criado_em_fim']
        editado_em_inicio = form.cleaned_data['editado_em_inicio']
        editado_em_fim = form.cleaned_data['editado_em_fim']

        # Filtro por título
        if titulo:
            posts = posts.filter(titulo__icontains=titulo)

        # Filtro por sumário
        if sumario:
            posts = posts.filter(sumario__icontains=sumario)

        # Filtro por data de criação (início)
        if criado_em_inicio:
            # Converte para datetime com fuso horário UTC
            criado_em_inicio = timezone.make_aware(datetime.combine(
                criado_em_inicio, datetime.min.time()))
            # Filtra pela data (sem hora) e usa __gte (maior ou igual)
            posts = posts.filter(criado_em__gte=criado_em_inicio)

        # Filtro por data de criação (fim)
        if criado_em_fim:
            # Converte para datetime com fuso horário UTC
            criado_em_fim = timezone.make_aware(datetime.combine(
                criado_em_fim, datetime.max.time()))
            # Filtra pela data (sem hora) e usa __lte (menor ou igual)
            posts = posts.filter(criado_em__lte=criado_em_fim)

        # Filtro por data de criação (inicio)
        if editado_em_inicio:
            # Converte para datetime com fuso horário UTC
            editado_em_inicio = timezone.make_aware(datetime.combine(
                editado_em_fim, datetime.min.time()))
            posts = posts.filter(editado_em__gte=editado_em_inicio)

        # Filtro por data de criação (fim)
        if editado_em_fim:
            # Converte para datetime com fuso horário UTC
            editado_em_fim = timezone.make_aware(datetime.combine(
                editado_em_fim, datetime.max.time()))
            posts = posts.filter(editado_em__lte=editado_em_fim)

    return render(request, 'sgc/post/listar_posts.html', {'posts': posts, 'form': form})


@login_required(login_url='/login')
@requires_csrf_token
@csrf_protect
def criar_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # print(request.user.autor_id)
            post = form.save(commit=False)
            matricula = request.user.email
            usuario = Usuario.objects.get(email=matricula)
            post.autor = usuario
            post.save()
            return redirect('listar_posts_view')
    else:
        form = PostForm()
    return render(request, 'sgc/post/criar_editar_post.html', {'form': form})


@login_required(login_url='/login')
@requires_csrf_token
@csrf_protect
def editar_post_view(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('listar_posts_view')
    else:
        form = PostForm(instance=post)
    return render(request, 'sgc/post/criar_editar_post.html', {'form': form, 'post': post})


@login_required(login_url='/login')
@requires_csrf_token
@csrf_protect
def deletar_post_view(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == 'POST':
        post.delete()
        return redirect('listar_posts_view')
    return render(request, 'sgc/post/deletar_post.html', {'post': post})


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


def logout_view(request):
    logout(request)
    return redirect(index)  # Redireciona para a página de login
