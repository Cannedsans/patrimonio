from django.contrib import admin
from .models import Categoria, Fornecedor, Departamento, Movimentacao
# Register your models here.
admin.site.register(Categoria)
admin.site.register(Departamento)
admin.site.register(Fornecedor)
admin.site.register(Movimentacao)
