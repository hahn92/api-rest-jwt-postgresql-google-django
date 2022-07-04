from django.http import JsonResponse
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .serializers import BooksSerializer
from .pagination import CustomPagination
from .permission import IsOwnerOrReadOnly
from .models import Books, Authors, Editors, Categories
import requests



class ListCreateBooksAPIView(ListCreateAPIView):
    """
    - Consulta libros
    - Crea una nueva tarea
    """
    serializer_class = BooksSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        search_text = self.request.GET.get('search_text')
        queryset = Books.objects.filter(Q(is_active=True) & Q(title__icontains=search_text) | Q(subtitle__icontains=search_text) | Q(subtitle__icontains=search_text))
        if queryset.count() == 0:
            return get_books_google(search_text)
        return queryset
        
    def perform_create(self, serializer):
        origen = self.request.data.get("origen", None)
        if origen == "google":
            get_books_google_by_id(self.request.data.get("origen_id", None))
            return True
        elif origen == "db":
            pass
        else:
            pass


class RetrieveUpdateDestroyBooksAPIView(RetrieveUpdateDestroyAPIView):
    """
    - Actualiza un libro
    - Elimina eliminar un libro
    """
    serializer_class = BooksSerializer
    queryset = Books.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


def get_books_google_by_id(id_book):
    api_root = 'https://www.googleapis.com'
    api = 'books'
    version = 'v1'
    api_url = api_root + '/' + api + '/' + version + '/volumes/' + id_book
    response = requests.get(api_url)
    books = []
    data = response.json()
    subtitle = ""
    if 'subtitle' in data['volumeInfo']:
        subtitle = data['volumeInfo']['subtitle']
    authors = ""
    if 'authors' in data['volumeInfo']:
        authors = data['volumeInfo']['authors']
    categories = ""
    if 'categories' in data['volumeInfo']:
        categories = data['volumeInfo']['categories']
    publishedDate = ""
    if 'publishedDate' in data['volumeInfo']:
        publishedDate = data['volumeInfo']['publishedDate']
    publisher = ""
    if 'publisher' in data['volumeInfo']:
        publisher = data['volumeInfo']['publisher']
    description = ""
    if 'description' in data['volumeInfo']:
        description = data['volumeInfo']['description']
    thumbnail = ""
    if 'imageLinks' in data['volumeInfo']:
        thumbnail = data['volumeInfo']['imageLinks']['thumbnail']
    books.append(set_object_books_save(data["id"], "google", data['volumeInfo']['title'], subtitle, authors, categories, publishedDate, publisher, description, thumbnail))
    return books


def set_object_books_save(id, origen, title, subtitle, authors, category, published_date, editor, description, image):
    
    if authors != "":
        autor = Authors.objects.filter(fullname__icontains=authors[0])
        if autor.count() == 0:
            Authors(
                fullname=authors[0]
            ).save()

    if category != "":
        categoria = Categories.objects.filter(name__icontains=category[0])
        if categoria.count() == 0:
            Categories(
                name=category[0]
            ).save()

    if editor != "":
        editors = Editors.objects.filter(name__icontains=editor)
        if editors.count() == 0:
            Editors(
                name=editor
            ).save()

    books = Books.objects.filter(external_id__icontains=id)
    if books.count() == 0:
        book = Books(
            external_id=id,
            origen=origen,
            title=title,
            subtitle=subtitle,
            published_date=published_date,
            description=description,
            picture=image
        ).save()
        book_new = Books.objects.get(external_id=id)
        if book_new:  
            autor = Authors.objects.filter(fullname__icontains=authors[0])
            book_new.books_author.add(autor[0])
            categoria = Categories.objects.filter(name__icontains=category[0])
            book_new.books_category.add(categoria[0])
            editor = Editors.objects.filter(name__icontains=editor)
            book_new.book_editor = editor[0]
            book_new.save()

        return True

    return False


def get_books_google(search_text):
    api_root = 'https://www.googleapis.com'
    api = 'books'
    version = 'v1'
    api_url = api_root + '/' + api + '/' + version + '/volumes?q=' + search_text
    response = requests.get(api_url)
    books = []
    for data in response.json()['items']:
        subtitle = ""
        if 'subtitle' in data['volumeInfo']:
            subtitle = data['volumeInfo']['subtitle']
        authors = ""
        if 'authors' in data['volumeInfo']:
            authors = data['volumeInfo']['authors']
        categories = ""
        if 'categories' in data['volumeInfo']:
            categories = data['volumeInfo']['categories']
        publishedDate = ""
        if 'publishedDate' in data['volumeInfo']:
            publishedDate = data['volumeInfo']['publishedDate']
        publisher = ""
        if 'publisher' in data['volumeInfo']:
            publisher = data['volumeInfo']['publisher']
        description = ""
        if 'description' in data['volumeInfo']:
            description = data['volumeInfo']['description']
        thumbnail = ""
        if 'imageLinks' in data['volumeInfo']:
            thumbnail = data['volumeInfo']['imageLinks']['thumbnail']
        books.append(set_object_books(data["id"], "google", data['volumeInfo']['title'], subtitle, authors, categories, publishedDate, publisher, description, thumbnail))
    return books
    

def set_object_books(id, origen, title, subtitle, authors, category, published_date, editor, description, image):
    autores = []
    categorias = []

    if authors != "":
        autores = Authors(
            fullname=authors[0]
        )
    if category != "":
        categorias = Categories(
            name=category[0]
        )
    editores = Editors(
        name=editor
    ).save()
    books = {
        'external_id': id,
        'origen': origen,
        'title':title,
        'subtitle':subtitle,
        'published_date':published_date,
        'book_editor':editores,
        'description':description,
        'picture':image,
        'books_category': [ categorias ],
        'books_author': [ autores ]
    }
    return books
