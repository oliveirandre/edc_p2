"""edc_p2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.tabela, name='jogadores'),
    path('tabela', views.tabela, name='tabela'),
    path('jogos', views.jogos, name='jogos'),
    path('jogadores', views.jogadores, name='jogadores'),
    path('jogo', views.jogo, name='jogo'),
    path('jogador', views.jogador, name='jogador'),
    path('equipa', views.infoclube, name='equipa'),
    path('editar_equipa', views.edit_club, name='editar_equipa'),
    path('edit', views.edit, name='edit'),
    path('req', views.req, name='req')

]
