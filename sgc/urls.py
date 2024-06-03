"""
URL configuration for sgc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import (cadastrar_usuario_view, login_view, logout_view, index, perfil_view,
                    processar_cadastro_aluno_view, processar_cadastro_professor_view,
                    criar_post_view, editar_post_view, listar_posts_view, deletar_post_view)

urlpatterns = [
    path(route='admin/', view=admin.site.urls),
    path(route='', view=index, name='index'),
    path(route='cadastrar/', view=cadastrar_usuario_view,
         name='cadastrar_usuario_view'),
    path('cadastrar/aluno/', processar_cadastro_aluno_view,
         name='processar_cadastro_aluno_view'),
    path('cadastrar/professor/', processar_cadastro_professor_view,
         name='processar_cadastro_professor_view'),
    path('/publicacao/criar/', criar_post_view,
         name='criar_post_view'),
    path(r'/publicacao/editar/<int:id>/', editar_post_view,
         name='editar_post_view'),
    path('/publicacao/todas/', listar_posts_view,
         name='listar_posts_view'),
    path('/publicacao/deletar/', deletar_post_view,
         name='deletar_post_view'),
    path(route='login/', view=login_view, name='login'),
    path(route='perfil/', view=perfil_view, name='perfil_view'),
    path(route='logout/', view=logout_view, name='logout'),
]
