from django.urls import path
from django.views.generic.base import RedirectView  # Importe o RedirectView
from .views import *

urlpatterns = [
    path('', RedirectView.as_view(url='bens/')),  # Redireciona '/' para '/bens/'
    path('bens/', home, name="bens"),
    path('login/', mlogin, name='login'),
    path('registrar', register, name='register'),
    path("logout/", logout_view, name="logout"),
    path('bens/novo', criar_bem, name='criar_bem'),
    path('bens/mover', mover_bem, name='mover_bem'),
    path('movimentacao/', movi, name = 'movimentacoes'),
    path('fonecedores/', fonece ,name = 'forne'),
    path('bens/editar/<str:id>/', editar_bem, name='editar_bem'),  # Nova URL para editar
    path('bens/agendar-manutencao/<str:id>/', agendar_manutencao, name='agendar_manutencao'),
    path('categorias/', categorias, name='categorias'),
]
