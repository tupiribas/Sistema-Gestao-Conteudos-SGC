from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.conf import settings
from gotrue.errors import AuthApiError

class SupabaseBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        supabase = settings.SUPABASE

        try:
            _response = supabase.auth.sign_in_with_password({"email": username, "password": password})

            if _response and _response.user:
                supabase_user = _response.user

                # Obtém ou cria o usuário no banco de dados do Django
                user, created = User.objects.get_or_create(username=supabase_user.id, defaults={
                    'email': supabase_user.email,
                    'first_name': supabase_user.user_metadata.get('first_name', ''),
                    'last_name': supabase_user.user_metadata.get('last_name', ''),
                })

                # Atualiza o token da sessão no banco de dados do Django, se necessário
                user.save()

                return user
            else:
                return None

        except AuthApiError as e:
            print(f"Erro de autenticação do Supabase")
            return e

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist as e:
            return e
