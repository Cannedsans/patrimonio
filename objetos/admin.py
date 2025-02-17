from django.contrib import admin
from .models import Categoria, Fornecedor, Departamento, Movimentacao, Manutencao

@admin.register(Manutencao)
class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ('bem', 'data_agendada', 'descricao', 'status')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['bem', 'data_agendada', 'descricao']
        return []

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    def get_fields(self, request, obj=None):
        if obj:
            return ['status']
        return ['bem', 'data_agendada', 'descricao', 'status']

@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('bem', 'de_departamento', 'para_departamento', 'data', 'responsavel')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

# Registrar os modelos sem personalização
admin.site.register(Categoria)
admin.site.register(Departamento)
admin.site.register(Fornecedor)