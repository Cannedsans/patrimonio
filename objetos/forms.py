from django import forms
from .models import *

class BemForm(forms.ModelForm):
    class Meta:
        model = Bem
        fields = ['id', 'nome', 'categoria', 'departamento', 'marca', 'valor','data_proxima_revisao']
        widget={
            "data_proxima_revisao" : forms.DateField()
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Obtém o usuário logado
        super().__init__(*args, **kwargs)

        # Adiciona classes Bootstrap aos campos do formulário
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        # Personaliza o campo ID (RFID)
        self.fields['id'].widget.attrs.update({
            'placeholder': '00:00:00:00',
            'maxlength': '11',
            'id': 'id_input'  # Definir ID para JS
        })

        # Personaliza o campo de valor
        self.fields['valor'].widget.attrs.update({
            'placeholder': '0.00',
            'step': '0.01',  # Permite valores decimais
        })

        # Personaliza o campo de data de próxima revisão
        self.fields['data_proxima_revisao'].widget.attrs.update({
            'type': 'date',  # Define como campo de data
        })

    def save(self, commit=True):
        bem = super().save(commit=False)
        if self.user:
            bem.dono = self.user  # Define o dono como o usuário logado
        if commit:
            bem.save()
        return bem

class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['bem', 'para_departamento']
        widgets = {
            'bem': forms.Select(attrs={'class': 'form-select'}),  # Estiliza com Bootstrap
            'para_departamento': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Captura o usuário logado
        super().__init__(*args, **kwargs)

        if user:
            self.fields['bem'].queryset = Bem.objects.filter(dono=user)  # Filtra apenas os bens do usuário

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True, user=None):  
        movimentacao = super().save(commit=False)

        if user:
            movimentacao.responsavel = user  # Define o responsável
        
        # Define o departamento de origem como o atual do bem
        movimentacao.de_departamento = movimentacao.bem.departamento  

        if commit:
            movimentacao.save()
            # Atualiza o departamento do bem após a movimentação ser salva
            movimentacao.bem.departamento = movimentacao.para_departamento
            movimentacao.bem.save()

        return movimentacao

class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        fields = ['data_agendada', 'descricao']
        widgets = {
            'data_agendada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona classes Bootstrap aos campos restantes
        for field_name, field in self.fields.items():
            if field_name != 'data_agendada':  # Evita sobrescrever o widget personalizado
                field.widget.attrs.update({'class': 'form-control'})

    