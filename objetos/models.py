from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=20)

    def __str__(self):
        return self.nome

class Departamento(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Bem(models.Model):
    MANUTENCAO_STATUS_CHOICES = [
        ('em_manutencao', 'Em Manutenção'),
        ('proximo_revisao', 'Próximo da Revisão'),
        ('ok', 'OK'),
    ]

    id = models.CharField(
        max_length=11,
        primary_key=True,
        validators=[
            RegexValidator(
                regex=r"^([0-9A-Fa-f]{2}):([0-9A-Fa-f]{2}):([0-9A-Fa-f]{2}):([0-9A-Fa-f]{2})$",
                message="O formato da tag RFID deve ser XX:XX:XX:XX (hexadecimal).",
            )
        ]
    )
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    dono = models.ForeignKey(User, on_delete=models.CASCADE)
    departamento = models.ForeignKey("Departamento", on_delete=models.CASCADE)
    marca = models.ForeignKey("Fornecedor", verbose_name="Marca", on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Valor do bem
    status_manutencao = models.CharField(max_length=20, choices=MANUTENCAO_STATUS_CHOICES, default='ok')  # Status de manutenção
    data_proxima_revisao = models.DateField(null=True, blank=True)  # Data da próxima revisão

    def __str__(self):
        return self.nome

class Fornecedor(models.Model):
    cnpj = models.CharField(
        max_length=18,
        primary_key=True,
        validators=[
            RegexValidator(
                regex=r"([0-9]{2}).([0-9]{3}).([0-9]{3})/([0-9]{4})-([0-9]{2})",
                message="O formato do CNPJ deve ser 00.000.000/0000-00",
            )
        ]
    )
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome}: {self.cnpj}"

class Movimentacao(models.Model):
    id = models.BigAutoField(primary_key=True)
    data = models.DateField(auto_now_add=True)
    bem = models.ForeignKey(Bem, on_delete=models.CASCADE)
    de_departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="movimentacoes_de")
    para_departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="movimentacoes_para")
    responsavel = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Movimentação de {self.bem.nome} de {self.de_departamento} para {self.para_departamento}"

class Patrimonio(models.Model):
    id = models.BigAutoField(primary_key=True)
    valor_total = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # Valor total do patrimônio
    data_atualizacao = models.DateField(auto_now=True)  # Data da última atualização do valor total

    def __str__(self):
        return f"Patrimônio Total: R$ {self.valor_total}"

class Manutencao(models.Model):
    STATUS_CHOICES = [
        ('agendada', 'Agendada'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
    ]

    bem = models.ForeignKey(Bem, on_delete=models.CASCADE, related_name='manutencoes')
    data_agendada = models.DateField()  # Data agendada para a manutenção
    descricao = models.TextField()  # Descrição da manutenção
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='agendada')  # Status da manutenção

    def __str__(self):
        return f"Manutenção de {self.bem.nome} em {self.data_agendada}"

    def save(self, *args, **kwargs):
        # Verifica se a manutenção está agendada ou em andamento
        if self.status in ['agendada', 'em_andamento']:
            # Atualiza o status do bem para "Em Manutenção"
            self.bem.status_manutencao = 'em_manutencao'
            self.bem.save()
        elif self.status == 'concluida':
            # Atualiza o status do bem para "OK" após a conclusão da manutenção
            self.bem.status_manutencao = 'ok'
            self.bem.save()
        super().save(*args, **kwargs)