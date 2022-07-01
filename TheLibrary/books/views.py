from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .serializers import BooksSerializer
from .pagination import CustomPagination
from .permission import IsOwnerOrReadOnly
from .models import Books


class ListCreateBooksAPIView(ListCreateAPIView):
    """
    - Consulta libros
    - Crea una nueva tarea
    """
    serializer_class = BooksSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = Books.objects.filter(is_active=True)
        return queryset
        
    def perform_create(self, serializer):
        serializer.save(books_register=self.request.user)


class RetrieveUpdateDestroyBooksAPIView(RetrieveUpdateDestroyAPIView):
    """
    - Actualiza una tarea
    - Elimina una tarea
    """
    serializer_class = BooksSerializer
    queryset = Books.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]