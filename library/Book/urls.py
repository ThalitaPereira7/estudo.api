from django.urls import path
from . import views

urlpatterns = [
    path('listar/adicionar/', views.listar_adicionar_livros, name='livros_listados'),
    path('api/books/', views.listar_livros, name='listar_livros'),
    path('api/books/<int:pk>/', views.detalhe_livro, name='detalhe_livro'),
    path('api/books/create/', views.criar_livro, name='criar_livro'),
    path('api/books/update/<int:pk>/', views.atualizar_livro, name='atualizar_livro'),
    path('api/books/delete/<int:pk>/', views.deletar_livro, name='deletar_livro'),
    path('api/register/', views.registrar_usuario, name='registrar_usuario'),

 
  
]

