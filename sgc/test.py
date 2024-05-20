import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL= os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print("Supabase client created successfully")

email = "juliaamorim7876@gmail.com"
senha = "123456"

resposta = supabase.auth.sign_in_with_password({
    "email": email,
    "password": senha,
})


user = resposta.user.id
print(user)


