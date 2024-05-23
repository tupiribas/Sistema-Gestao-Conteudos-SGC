import os
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock
from supabase import create_client, Client as SupabaseClient
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = DjangoClient()

    @patch('supabase.create_client')
    def test_login_success(self, mock_create_client):
        # Configurar o mock para simular uma autenticação bem-sucedida
        mock_supabase = MagicMock()
        mock_user = MagicMock()
        mock_user.id = '1'
        mock_user.email = 'test@example.com'

        mock_supabase.auth.sign_in_with_password.return_value = {
            'user': mock_user,
            'session': None,  # Não precisamos da sessão para este teste
        }
        mock_create_client.return_value = mock_supabase

        # Enviar uma requisição POST para a view de login
        response = self.client.post(reverse('login'), {'email': 'emaildecontas002@gmail.com', 'password': 'testpassword'})

        # Verificar se o usuário foi autenticado
        self.assertEqual(response.status_code, 302)  # Redirecionamento para a página inicial
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.email, 'emaildecontas002@gmail.com')

    @patch.object(SupabaseClient, 'auth')
    def test_login_failure(self, mock_auth):
        # Configurar o mock para simular uma autenticação com falha
        mock_auth.sign_in_with_password.return_value = {
            'error': {'message': 'Invalid login credentials'}
        }

        # Enviar uma requisição POST para a view de login
        response = self.client.post(reverse('login'), {'email': 'emaildecontas002@gmail.com', 'password': 'wrongpassword'})

        # Verificar se a mensagem de erro foi adicionada
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), 'Erro ao fazer login no Supabase: Invalid login credentials')
