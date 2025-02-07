from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=20)  # Substituí TextField por CharField

    def __str__(self):
        return self.nome

class Departamento(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)  # Substituí TextField por CharField

    def __str__(self):
        return self.nome

class Bem(models.Model):
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
    nome = models.CharField(max_length=100)  # Substituí TextField por CharField
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    dono = models.ForeignKey(User, on_delete=models.CASCADE)
    departamento = models.ForeignKey("Departamento", on_delete=models.CASCADE)  # Adicionado aspas para evitar erro de referência

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
    nome = models.CharField(max_length=100)  # Substituí TextField por CharField

    def __str__(self):
        return f"{self.nome}: {self.cnpj}"

class Movimentacao(models.Model):
    id = models.BigAutoField(primary_key=True)
    data = models.DateField(auto_now_add=True)  # Removido auto_now=True
    bem = models.ForeignKey(Bem, on_delete=models.CASCADE)
    de_departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="movimentacoes_de")
    para_departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="movimentacoes_para")
    responsavel = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Movimentação de {self.bem.nome} de {self.de_departamento} para {self.para_departamento}"
