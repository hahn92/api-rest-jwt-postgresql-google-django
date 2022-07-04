# Django
from django.db import models
# Traductor a diferentes idiomas nativo
from django.utils.translation import gettext as _ 

# Custom User
from django.contrib.auth import get_user_model
User = get_user_model()

class TemplateBooks(models.Model):

    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo',
    )
    # Logs
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creado'
    )
    modified = models.DateTimeField(
        auto_now=True,
        verbose_name='Modificado'
    )

    class Meta:
        abstract = True

#########################################################################


class Authors(TemplateBooks):
    """
    Modelo Autores
    """
    fullname = models.CharField(
        max_length=50,
        default="",
        blank=False,
        null=False,
        verbose_name='Nombre(s)',
    )
    
    def __str__(self):
        return self.fullname

    class Meta:
        ordering = ('fullname',)
        verbose_name = _('Autor')
        verbose_name_plural = _('Autores')
        permissions = (
            ("view_all_authors", "Can view all authors"),
        )


class Editors(TemplateBooks):
    """
    Modelo Editoriales
    """
    name = models.CharField(
        max_length=50,
        default="",
        blank=False,
        null=False,
        verbose_name='Editorial',
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Editorial'
        verbose_name_plural = 'Editoriales'
        permissions = (
            ("view_all_editors", "Can view all editors"),
        )


class Categories(TemplateBooks):
    """
    Modelo Categorias
    """
    name = models.CharField(
        max_length=50,
        default="",
        blank=False,
        null=False,
        verbose_name='Categoria',
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        permissions = (
            ("view_all_categoties", "Can view all categories"),
        )


class Books(TemplateBooks):
    """
    Modelo Libros
    """
    external_id = models.CharField(
        max_length=20,
        default="",
        blank=False,
        null=False,
        verbose_name='Id API externa',
    )
    origen = models.CharField(
        max_length=20,
        default="db interna",
        blank=False,
        null=False,
        verbose_name='Origen',
    )
    title = models.CharField(
        max_length=50,
        default="",
        blank=False,
        null=False,
        verbose_name='Titulo',
    )
    subtitle = models.CharField(
        max_length=50,
        default="",
        blank=False,
        null=False,
        verbose_name='Sub-Titulo',
    )
    books_author = models.ManyToManyField(
        Authors,
        related_name="books_author",
        blank=False,
        default="",
        verbose_name='Autor(es)',
    )
    books_category = models.ManyToManyField(
        Categories,
        related_name="tasks_category",
        blank=False,
        default="",
        verbose_name='Categoria(s)',
    )
    published_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Fecha de publicación',
    )
    book_editor = models.ForeignKey(
        Editors,
        related_name="book_editor",
        blank=True,
        null=True,
        default="",
        on_delete=models.SET_DEFAULT,
        verbose_name='Editorial',
    )
    description = models.TextField(
        max_length=500,
        default="",
        blank=True,
        null=True,
        verbose_name='Descripción',
    )
    picture = models.ImageField(
        upload_to='books/pictures',
        blank=True,
        null=True,
        verbose_name=_('Imagen')
    )
    books_register = models.ForeignKey(
        User,
        related_name="book_editor",
        blank=True,
        null=True,
        default="",
        on_delete=models.SET_DEFAULT,
        verbose_name='Registrado por',
    )

    def __str__(self):
        return self.title

    def get_authors(self):
        return ", ".join([author.fullname for author in self.books_author.all()])

    def get_categories(self):
        return ", ".join([category.name for category in self.books_category.all()])

    class Meta:
        ordering = ('title',)
        verbose_name = _('Libro')
        verbose_name_plural = _('Libros')
        permissions = (
            ("view_all_books", "Can view all books"),
        )


