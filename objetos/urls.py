from django.urls import path
from .views import *

urlpatterns = [
    path('bens/', home, name="bens"),
    path('login/', mlogin, name='login'),
    path('registrar', register, name='register'),
    path("logout/", logout_view, name="logout"),
    path('bens/novo', criar_bem, name='criar_bem'),
    path('bens/mover', mover_bem, name='mover_bem'),
    path('movimentacao/', movi, name = 'movimentacoes'),
    path('fonecedores/', fonece ,name = 'forne'),
]
