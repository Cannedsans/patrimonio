from django import forms
from .models import *

class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['bem', 'para_departamento']
        widgets = {
            'bem': forms.Select(attrs={'class': 'form-select'}),
            'para_departamento': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Captura o usuário passado na view
        super().__init__(*args, **kwargs)

        if user:
            # Filtra apenas os bens do usuário logado
            self.fields['bem'].queryset = Bem.objects.filter(dono=user)

    def save(self, commit=True, user=None):  
        movimentacao = super().save(commit=False)

        if user:
            movimentacao.responsavel = user  # O responsável será o usuário logado
        
        # Define o departamento de origem como o atual do bem
        movimentacao.de_departamento = movimentacao.bem.departamento  
        
        if commit:
            movimentacao.save()
            # Atualiza o departamento do bem após a movimentação ser salva
            movimentacao.bem.departamento = movimentacao.para_departamento
            movimentacao.bem.save()

        return movimentacao
