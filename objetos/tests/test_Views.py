from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from objetos.models import *
from objetos.views import *
from django.urls import reverse
from django.contrib.messages import get_messages

class HomeViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Criar objetos relacionados necessários
        self.categoria = Categoria.objects.create(nome="Eletrônicos")
        self.departamento = Departamento.objects.create(nome="TI")
        self.fornecedor_user = User.objects.create_user(username='fornecedor', password='12345')
        self.fornecedor = Fornecedor.objects.create(
            cnpj="12.345.678/0001-99",
            userId=self.fornecedor_user,
            nome="Fornecedor Teste"
        )
        self.bem = Bem.objects.create(
            id="AB:CD:12:34",
            nome="Bem Teste",
            categoria=self.categoria,
            dono=self.user,
            departamento=self.departamento,
            marca=self.fornecedor
        )

    def test_home_view_authenticated(self):
        request = self.factory.get('/bens/')
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code, 200)

class RegisterViewTest(TestCase):
    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_view_post_success(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)  # Redireciona para login
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_view_post_password_mismatch(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'wrongpassword',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)  # Permanece na página de registro
        self.assertFalse(User.objects.filter(username='newuser').exists())


class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post_success(self):
        data = {
            'username': 'testuser',
            'password': '12345',
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)  # Redireciona para 'bens'

    def test_login_view_post_failure(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)  # Permanece na página de login
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Usuário ou senha inválidos.")


class CriarBemViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        # Criar objetos relacionados necessários
        self.categoria = Categoria.objects.create(nome="Eletrônicos")
        self.departamento = Departamento.objects.create(nome="TI")
        self.fornecedor_user = User.objects.create_user(username='fornecedor', password='12345')
        self.fornecedor = Fornecedor.objects.create(
            cnpj="12.345.678/0001-99",
            userId=self.fornecedor_user,
            nome="Fornecedor Teste"
        )

    def test_criar_bem_view_get(self):
        response = self.client.get(reverse('criar_bem'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_criar_bem_view_post_success(self):
        data = {
            'id': 'AB:CD:12:34',  # Formato válido
            'nome': 'Novo Bem',
            'categoria': self.categoria.id,
            'dono': self.user.id,
            'departamento': self.departamento.id,
            'marca': self.fornecedor.cnpj,  # CNPJ como chave primária
        }
        response = self.client.post(reverse('criar_bem'), data)
        self.assertEqual(response.status_code, 200)  # Redireciona para 'bens'


class MoverBemViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        # Criar objetos relacionados necessários
        self.categoria = Categoria.objects.create(nome="Eletrônicos")
        self.departamento = Departamento.objects.create(nome="TI")
        self.fornecedor_user = User.objects.create_user(username='fornecedor', password='12345')
        self.fornecedor = Fornecedor.objects.create(
            cnpj="12.345.678/0001-99",
            userId=self.fornecedor_user,
            nome="Fornecedor Teste"
        )
        self.bem = Bem.objects.create(
            id="AB:CD:12:34",
            nome="Bem Teste",
            categoria=self.categoria,
            dono=self.user,
            departamento=self.departamento,
            marca=self.fornecedor
        )

    def test_mover_bem_view_get(self):
        response = self.client.get(reverse('mover_bem'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_mover_bem_view_post_success(self):
        data = {
            'bem': self.bem.id,
            'novo_dono': self.user.id,
        }
        response = self.client.post(reverse('mover_bem'), data)
        self.assertEqual(response.status_code, 200)  # Redireciona para 'bens'


class MoviViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        # Criar objetos relacionados necessários
        self.categoria = Categoria.objects.create(nome="Eletrônicos")
        self.departamento = Departamento.objects.create(nome="TI")
        self.fornecedor_user = User.objects.create_user(username='fornecedor', password='12345')
        self.fornecedor = Fornecedor.objects.create(
            cnpj="12.345.678/0001-99",
            userId=self.fornecedor_user,
            nome="Fornecedor Teste"
        )
        self.bem = Bem.objects.create(
            id="AB:CD:12:34",
            nome="Bem Teste",
            categoria=self.categoria,
            dono=self.user,
            departamento=self.departamento,
            marca=self.fornecedor
        )
        self.movimentacao = Movimentacao.objects.create(
            bem=self.bem,
            de_departamento=self.departamento,
            para_departamento=self.departamento,
            responsavel=self.user
        )

    def test_movi_view(self):
        response = self.client.get(reverse('movimentacoes'))
        self.assertEqual(response.status_code, 200)

class FoneceViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.fornecedor = Fornecedor.objects.create(
            cnpj="12.345.678/0001-99",
            userId=self.user,
            nome="Fornecedor Teste"
        )

    def test_fonece_view(self):
        response = self.client.get(reverse('forne'))
        self.assertEqual(response.status_code, 302)
