from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

@login_required
def home(request):
    bens = Bem.objects.filter(dono=request.user)  # Mostra apenas os bens do usuário logado
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