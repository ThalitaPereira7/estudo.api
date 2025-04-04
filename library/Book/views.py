from django.shortcuts import render, redirect
from . models import Book, CustomUser
from .forms import LivroForm
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import BookSerializer, CustomUserSerializer
from rest_framework.permissions import IsAuthenticated
from datetime import datetime


def listar_adicionar_livros(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            print("Deu certo")
            return redirect('livros_listados')  # Redireciona após salvar
    
    livros = Book.objects.all()
    form = LivroForm()  # Formulário vazio para GET
    return render(request, 'library/book_list.html', {
        'livros': livros,
        'form': form
    })
    
    
@api_view(['GET'])
def listar_livros(request):
    author = request.query_params.get('author')
    published_date = request.query_params.get('published_date')
    quantidade = request.query_params.get('quantidade')
    ordenar = request.query_params.get('ordenar')

    queryset = Book.objects.all()

    if author:
        queryset = queryset.filter(author__icontains=author)
    if published_date:
        try:
            data = datetime.strptime(published_date, "%Y-%m-%d").date()
            queryset = queryset.filter(published_date=data)
        except ValueError:
            return Response({'erro': 'Data inválida, use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
    if quantidade:
        try:
            quantidade = int(quantidade)
            queryset = queryset[:quantidade]
        except ValueError:
            return Response({'erro': 'Quantidade deve ser um número inteiro'}, status=status.HTTP_400_BAD_REQUEST)
    if ordenar:
        queryset = queryset.order_by(ordenar)

    serializer = BookSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def detalhe_livro(request, pk):
    try:
        livro = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({'erro': 'Livro não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = BookSerializer(livro)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def criar_livro(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        if Book.objects.filter(isbn=serializer.validated_data['isbn']).exists():
            return Response({'erro': 'ISBN já existe'}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.validated_data['published_date'] > datetime.now().date():
            return Response({'erro': 'Data de publicação não pode ser no futuro'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def atualizar_livro(request, pk):
    try:
        livro = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({'erro': 'Livro não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = BookSerializer(livro, data=request.data)
    if serializer.is_valid():
        if serializer.validated_data['published_date'] > datetime.now().date():
            return Response({'erro': 'Data de publicação não pode ser no futuro'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletar_livro(request, pk):
    try:
        livro = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({'erro': 'Livro não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    livro.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def registrar_usuario(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
