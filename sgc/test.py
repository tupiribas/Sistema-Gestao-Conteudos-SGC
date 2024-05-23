from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock
from supabase import create_client, Client as SupabaseClient
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = SupabaseClient()

    @patch.object(SupabaseClient, 'auth')
    def test_login_success(self, mock_auth):
        # Configurar o mock para simular uma autenticação bem-sucedida
        mock_user = MagicMock()
        mock_user.id = '1'
        mock_user.email = 'test@example.com'
        mock_user.password = "123456"

        mock_auth.sign_in_with_password.return_value = {
            'user': mock_user,
            'session': None,  # Não precisamos da sessão para este teste
        }

        # Enviar uma requisição POST para a view de login
        response = self.client.post(reverse('login'), {'email': 'test@example.com', 'password': 'testpassword'})

        # Verificar se o usuário foi autenticado
        self.assertEqual(response.status_code, 302)  # Redirecionamento para a página inicial
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.email, 'test@example.com')

    @patch.object(SupabaseClient, 'auth')
    def test_login_failure(self, mock_auth):
        # Configurar o mock para simular uma autenticação com falha
        mock_auth.sign_in_with_password.return_value = {
            'error': {'message': 'Invalid login credentials'}
        }

        # Enviar uma requisição POST para a view de login
        response = self.client.post(reverse('login'), {'email': 'test@example.com', 'password': 'wrongpassword'})

        # Verificar se a mensagem de erro foi adicionada
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), 'Erro ao fazer login no Supabase: Invalid login credentials')
