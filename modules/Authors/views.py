from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Author
from .serializers import AuthorSerializer,AuthorBookSerializer
from django.db.models import Q
#Clases bsadas en vistas o "Clased base views"

class AuthorList(APIView):
    """
    get:
    Obtine todos los autores

    post:
    Crea un nuevo autor
    """
    def get(self,request):
        gender = request.query_params.get('gender')
        is_alive = request.query_params.get('is_alive')
        nationality = request.query_params.get('nationality')
        if (gender or is_alive or nationality) is not None:
            authors = Author.objects.filter(Q(gender__icontains=gender) |
                Q(is_alive=bool(is_alive)) |
                Q(nationality__icontains=nationality)
            )
            serializer = AuthorSerializer(authors,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)

        else:
            authors = Author.objects.all()
            serializer = AuthorBookSerializer(authors,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)

    
    def post(self,request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


#localhost:8000/api/v1/authors/

class AuthorDetail(APIView):
#localhost:8000/api/v1/authors/1/

    # def _get_author(self,pk):
    #     try:
    #         autor = Author.objects.get(id=pk)
    #         return autor
    #     except Author.DoesNotExist:
    #         raise Http404


    def get(self,request,pk):
        autor = get_object_or_404(Author,id=pk)
        serializer = AuthorSerializer(autor)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        autor = get_object_or_404(Author,id=pk)
        serializer = AuthorSerializer(autor,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
    
    def delete(self,request,pk):
        autor = get_object_or_404(Author,id=pk)
        autor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

