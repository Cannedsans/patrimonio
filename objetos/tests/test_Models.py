from django.test import TestCase
from django.contrib.auth.models import User
from objetos.models import *
from django.core.exceptions import ValidationError

# Teste para Categoria
class TestCategoria(TestCase):
    def setUp(self):
        self.categoria1 = Categoria.objects.create(nome="Dummy")

    def test_nomeCategoria(self):
        """Testa se o nome da categoria é retornado corretamente."""
        self.assertEqual(str(self.categoria1), "Dummy")


# Teste para Departamento
class TestDepartamento(TestCase):
    def setUp(self):
        self.depo1 = Departamento.objects.create(nome="Dummy")

    def test_nomeDepartamento(self):
        """Testa se o nome do departamento é retornado corretamente."""
        self.assertEqual(str(self.depo1), "Dummy")


# Teste para Bem
class TestBem(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Mítico")
        self.dono = User.objects.create_user(
            username='teste',
            email='teste@example.com',
            password='senha123'
        )
        self.departamento = Departamento.objects.create(nome="Dummy")
        self.fornecedor = Fornecedor.objects.create(
            cnpj="12.345.678/0001-99",
            userId=self.dono,
            nome="Fornecedor Exemplo"
        )

    def test_rfid_invalido(self):
        """Testa se um RFID inválido gera um erro de validação."""
        with self.assertRaises(ValidationError):
            bem = Bem(
                id="a123",  # Formato inválido
                nome="Bem Inválido",
                categoria=self.categoria,
                dono=self.dono,
                departamento=self.departamento,
                marca=self.fornecedor
            )
            bem.full_clean()  # Dispara a validação

    def test_criado(self):
        """Testa se um RFID válido é aceito e armazenado corretamente."""
        bem = Bem.objects.create(
            id="D3:FD:44:FA",  # Formato válido
            nome="Bem válido",
            categoria=self.categoria,
            dono=self.dono,
            departamento=self.departamento,
            marca=self.fornecedor
        )
        self.assertEqual(bem.id, "D3:FD:44:FA")
        self.assertEqual(str(bem), bem.nome)


# Teste para Fornecedores
class TestFornecedores(TestCase):
    def setUp(self):
        # Criando um usuário para o fornecedor
        self.user = User.objects.create_user(
            username='fornecedor_teste',
            email='fornecedor@example.com',
            password='senha123'
        )
        # Criando um fornecedor válido
        self.fornecedor = Fornecedor.objects.create(
            cnpj="12.345.678/0001-99",  # Formato válido
            userId=self.user,
            nome="Fornecedor Exemplo"
        )

    def test_cnpj_invalido(self):
        """Testa se um CNPJ inválido gera um erro de validação."""
        with self.assertRaises(ValidationError):
            fornecedor = Fornecedor(
                cnpj="123456789",  # Formato inválido
                userId=self.user,
                nome="Fornecedor Inválido"
            )
            fornecedor.full_clean()  # Dispara a validação

    def test_criado(self):
        """Testa se um fornecedor válido é aceito e armazenado corretamente."""
        # Verificando se o CNPJ foi armazenado corretamente
        self.assertEqual(self.fornecedor.cnpj, "12.345.678/0001-99")
        # Verificando se a string de representação do fornecedor está correta
        self.assertEqual(str(self.fornecedor), "Fornecedor Exemplo: 12.345.678/0001-99")


# Teste para Movimentações
class TestMovimentacoes(TestCase):
    def setUp(self):
        # Criar categorias, usuários, departamentos, e bens para o teste
        self.categoria = Categoria.objects.create(nome="Eletrônicos")
        self.dono = User.objects.create_user(
            username='usuario_teste',
            email='usuario@example.com',
            password='senha123'
        )
        self.depto_origem = Departamento.objects.create(nome="TI")
        self.depto_destino = Departamento.objects.create(nome="Administração")
        self.fornecedor = Fornecedor.objects.create(
            cnpj="12.345.678/0001-99",
            userId=self.dono,
            nome="Fornecedor Exemplo"
        )
        self.bem = Bem.objects.create(
            id="AB:CD:12:34",
            nome="Notebook",
            categoria=self.categoria,
            dono=self.dono,
            departamento=self.depto_origem,
            marca=self.fornecedor
        )
        self.movimentacao = Movimentacao.objects.create(
            bem=self.bem,
            de_departamento=self.depto_origem,
            para_departamento=self.depto_destino,
            responsavel=self.dono
        )

    def test_criado(self):
        """Testa se a movimentação foi criada corretamente."""
        self.assertEqual(self.movimentacao.bem, self.bem)
        self.assertEqual(self.movimentacao.de_departamento, self.depto_origem)
        self.assertEqual(self.movimentacao.para_departamento, self.depto_destino)
        self.assertEqual(self.movimentacao.responsavel, self.dono)
        self.assertIsNotNone(self.movimentacao.data)  # Verifica se a data foi criada automaticamente