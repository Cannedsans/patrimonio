from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

@login_required
def home(request):
    bens = Bem.objects.filter(dono=request.user)  # Mostra apenas os bens do usuário logado

    valor_total = sum(bem.valor for bem in bens)
    return render(request, 'show.html', {
        'bens': bens,
        'valor_total': valor_total,
    })
    return render(request, "show.html", {"bens": bens})

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "As senhas não coincidem.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Nome de usuário já existe.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Este email já está em uso.")
            return redirect("register")

        # Criando o usuário
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        
        messages.success(request, "Cadastro realizado com sucesso! Faça login.")
        return redirect("login")  # Redireciona para a página de login

    return render(request, "register.html")

def mlogin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login realizado com sucesso!")
            return redirect("bens")  
        else:
            messages.error(request, "Usuário ou senha inválidos.")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Logout realizado com sucesso!")
    return redirect("login")  

@login_required
def criar_bem(request):
    if request.method == "POST":
        form = BemForm(request.POST, user=request.user)  # 🔹 Passando `user`
        if form.is_valid():
            form.save()
            return redirect('bens')
    else:
        form = BemForm(user=request.user)  # 🔹 Passando `user` também aqui

    return render(request, 'form.html', {'form': form, 'titulo': 'Criar Bem'})


@login_required
def mover_bem(request):
    if request.method == "POST":
        form = TransacaoForm(request.POST, user=request.user)  # Passa o usuário autenticado
        if form.is_valid():
            form.save(user=request.user)  
            messages.success(request, "Bem transferido com sucesso!")
            return redirect('bens')  
    else:
        form = TransacaoForm(user=request.user)  # Passa o usuário ao criar o formulário vazio

    return render(request, 'form.html', {'form': form, 'titulo': 'Mover Bem'})

@login_required
def movi(request):
    movi = Movimentacao.objects.filter(bem__dono=request.user)  # Mostra apenas os bens do usuário logado
    return render(request, "show.html", {"movi": movi})

@login_required
def fonece(request):
    forne = Fornecedor.objects.all()
    return render(request, "show.html", {"forne":forne})

@login_required
def editar_bem(request, id):
    # Obtém o bem com base no ID ou retorna 404 se não existir
    bem = get_object_or_404(Bem, id=id)

    # Verifica se o usuário logado é o dono do bem
    if bem.dono != request.user:
        return redirect('bens')  # Redireciona se o usuário não for o dono

    if request.method == 'POST':
        # Preenche o formulário com os dados enviados e a instância do bem
        form = BemForm(request.POST, instance=bem, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('bens')  # Redireciona para a lista de bens após salvar
    else:
        # Exibe o formulário preenchido com os dados do bem
        form = BemForm(instance=bem, user=request.user)

    return render(request, 'form.html', {
        'form': form,
        'titulo': 'Editar Bem'
    })

def agendar_manutencao(request, id):
    # Obtém o bem com base no ID ou retorna 404 se não existir
    bem = get_object_or_404(Bem, id=id)

    # Verifica se o usuário logado é o dono do bem
    if bem.dono != request.user:
        return redirect('bens')  # Redireciona se o usuário não for o dono

    if request.method == 'POST':
        # Preenche o formulário com os dados enviados
        form = ManutencaoForm(request.POST)
        if form.is_valid():
            manutencao = form.save(commit=False)
            manutencao.bem = bem  # Associa a manutenção ao bem
            manutencao.save()
            return redirect('bens')  # Redireciona para a lista de bens após salvar
    else:
        # Exibe o formulário vazio
        form = ManutencaoForm()

    return render(request, 'form.html', {
        'form': form,
        'titulo': f'Agendar Manutenção para {bem.nome}'
    })

@login_required
def categorias(request):
    # Recupera todas as categorias do banco de dados
    categorias = Categoria.objects.all()
    return render(request, 'show.html', {
        'categorias': categorias,  # Passa as categorias para o template
        'titulo': 'Categorias'  # Título da página
    })