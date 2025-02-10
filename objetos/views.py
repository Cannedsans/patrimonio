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
    return render(request, 'register.html')

def mlogin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login realizado com sucesso!")
            return redirect("index")  
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
        form = BemForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)  
            messages.success(request, "Bem criado com sucesso!")
            return redirect('index')  
    else:
        form = BemForm()

    return render(request, 'form.html', {'form': form, 'titulo': 'Criar Bem'})

@login_required
def mover_bem(request):
    if request.method == "POST":
        form = TransacaoForm(request.POST, user=request.user)  # Passa o usuário autenticado
        if form.is_valid():
            form.save(user=request.user)  
            messages.success(request, "Bem transferido com sucesso!")
            return redirect('index')  
    else:
        form = TransacaoForm(user=request.user)  # Passa o usuário ao criar o formulário vazio

    return render(request, 'form.html', {'form': form, 'titulo': 'Mover Bem'})

@login_required
def movi(request):
    movi = Movimentacao.objects.filter(bem__dono=request.user)  # Mostra apenas os bens do usuário logado
    return render(request, "show.html", {"movi": movi})