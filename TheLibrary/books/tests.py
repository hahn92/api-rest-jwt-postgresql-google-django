# Django
from django.test import TestCase

# Python
import json

# Django Rest Framework
from rest_framework.test import APIClient
from rest_framework import status


# Custom User
from django.contrib.auth import get_user_model
User = get_user_model()    


# Models
from .models import Books, Authors, Editors, Categories

class BooksTestCase(TestCase):

    def setUp(self):
        """
        Setup para las pruebas
        """
        user = User(
            username='admin'
        )
        user.set_password('admin123')
        user.save()

        client = APIClient()
        response = client.post(
                '/api/token/', {
                'username': 'admin',
                'password': 'admin123',
            },
            format='json'
        )

        result = json.loads(response.content)
        self.user = user
        self.access = result['access']
        self.refresh = result['refresh']

        """
        Vuevo Libro
        """
        autor = Authors.objects.create(
            fullname='Autor 1'
        ).save()
        categoria = Categories.objects.create(
            name='Categoria 1'
        ).save()
        editor = Editors.objects.create(
            name='Editor 1'
        ).save()
        libro = Books.objects.create(
            title='Libro de prueba',
            subtitle='Subtitulo de prueba',
            description='Descripcion de prueba',
            picture='http://www.etnassoft.com/img/logo.png',
            published_date='2020-01-01',
            origen='db interno',
            external_id='12345',
            books_register=user
        ).save()
        nuevo_libro = Books.objects.filter(external_id='12345').first()
        nuevo_libro.books_author.add(autor)
        nuevo_libro.books_category.add(categoria)
        nuevo_libro.book_editor = editor
        nuevo_libro.save()
        self.book = nuevo_libro
    

    def test_create_book(self):
        """
        Crear un libro
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)

        test_book = {
            "origen": "google",
            "origen_id": "8y0yzQEACAAJ",
        }

        response = client.post(
            '/api/v1/books/', 
            test_book,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

  
    def test_delete_books(self):
        """
        Eliminar un libro
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)

        """
        Nuevo Libro
        """
        autor = Authors.objects.create(
            fullname='Autor 2'
        ).save()
        categoria = Categories.objects.create(
            name='Categoria 2'
        ).save()
        editor = Editors.objects.create(
            name='Editor 2'
        ).save()
        Books.objects.create(
            title='Libro de prueba 2',
            subtitle='Subtitulo de prueba 2',
            description='Descripcion de prueba 2',
            picture='http://www.etnassoft.com/img/logo.png',
            published_date='2020-01-01',
            origen='db interno',
            external_id='54321',
            books_register=self.user
        ).save()
        nuevo_libro = Books.objects.filter(external_id='54321').first()
        nuevo_libro.books_author.add(autor)
        nuevo_libro.books_category.add(categoria)
        nuevo_libro.book_editor = editor
        nuevo_libro.save()

        response = client.delete(
            f'/api/v1/books/{nuevo_libro.pk}', 
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        books_exists = Books.objects.filter(pk=nuevo_libro.pk)
        self.assertFalse(books_exists)


    def test_search_books_interno(self):
        """
        Obtener un libro database interno
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)

        """
        Nuevo Libro
        """
        autor = Authors.objects.create(
            fullname='Autor 3'
        ).save()
        categoria = Categories.objects.create(
            name='Categoria 3'
        ).save()
        editor = Editors.objects.create(
            name='Editor 3'
        ).save()
        Books.objects.create(
            title='Libro de prueba 3',
            subtitle='Subtitulo de prueba 3',
            description='Descripcion de prueba 3',
            picture='http://www.etnassoft.com/img/logo.png',
            published_date='2020-01-01',
            origen='db interno',
            external_id='54321',
            books_register=self.user
        ).save()
        nuevo_libro = Books.objects.filter(external_id='54321').first()
        nuevo_libro.books_author.add(autor)
        nuevo_libro.books_category.add(categoria)
        nuevo_libro.book_editor = editor
        nuevo_libro.save()

        response = client.get('/api/v1/books/?search_text=Libro&origen=google')
        
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result["results"][0]["title"], 'Libro de prueba')
        self.assertEqual(result["results"][0]["origen"], 'db interno')
        self.assertEqual(len(result), 4)

        
    def test_search_books_external_google(self):
        """
        Obtener un libro database externa google
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)

        response = client.get('/api/v1/books/?search_text=Casa&origen=google')
        
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result["results"][0]["origen"], 'google')
        self.assertEqual(len(result), 4)

             
    def test_search_books_external_openlibra(self):
        """
        Obtener un libro database external openlibra
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)

        response = client.get('/api/v1/books/?search_text=Cienc&origen=openlibra')
        
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result["results"][0]["origen"], 'openlibra')
        self.assertEqual(len(result), 4)

   