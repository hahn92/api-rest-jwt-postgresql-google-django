from django.contrib import admin

# Models
from .models import Books, Authors, Editors, Categories

@admin.register(Authors)
class AuthorsAdmin(admin.ModelAdmin):
    """
    Vista Authors en administrador
    """
    list_display = ('pk', 'fullname', "is_active", "created", "modified")
    list_display_links = ('pk', 'fullname',)

    search_fields = (
        'fullname',
    )

    list_filter = (
        'is_active',
        'created',
        'modified',
    )

    fieldsets = (
        ('Datos basicos', {
            'fields': (
                ('fullname', 'is_active',)
            ),
        }),
        ('Metadatos', {
            'fields': ('created', 'modified',),
        })
    )

    readonly_fields = ('created', 'modified',)


@admin.register(Editors)
class EditorsAdmin(admin.ModelAdmin):
    """
    Vista Editors en administrador
    """
    list_display = ('pk', 'name', "is_active", "created", "modified")
    list_display_links = ('pk', 'name',)

    search_fields = (
        'name',
    )

    list_filter = (
        'is_active',
        'created',
        'modified',
    )

    fieldsets = (
        ('Datos basicos', {
            'fields': (
                ( 'name', 'is_active',)
            ),
        }),
        ('Metadatos', {
            'fields': ('created', 'modified',),
        })
    )

    readonly_fields = ('created', 'modified',)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    """
    Vista Categories en administrador
    """
    list_display = ('pk', 'name', "is_active", "created", "modified")
    list_display_links = ('pk', 'name',)

    search_fields = (
        'name',
    )

    list_filter = (
        'is_active',
        'created',
        'modified',
    )

    fieldsets = (
        ('Datos basicos', {
            'fields': (
                ( 'name', 'is_active',)
            ),
        }),
        ('Metadatos', {
            'fields': ('created', 'modified',),
        })
    )

    readonly_fields = ('created', 'modified',)


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    """
    Vista Books en administrador
    """
    list_display = ('pk', 'external_id', 'origen', 'title', "subtitle", "get_authors", "get_categories", "published_date", "book_editor", "description", "picture", "books_register", "created", "modified")
    list_display_links = ('pk', 'title',)

    search_fields = (
        'title',
        'description',
        'books_author__username',
    )

    list_filter = (
        'is_active',
        'published_date',
        'created',
        'modified',
    )

    fieldsets = (
        ('Datos basicos', {
            'fields': (
                ( 'title', 'subtitle', 'is_active',), 
                ( 'books_author', 'published_date', 'books_category',), 
                ( 'book_editor', 'picture',), 
                'description', 
            ),
        }),
        ('Metadatos', {
            'fields': (
                ('external_id', 'origen', 'books_register',),
                ('created', 'modified',),
                ),
        })
    )

    autocomplete_fields = ['books_author']
    filter_horizontal = ('books_category',)
    readonly_fields = ('books_register', 'external_id', 'origen', 'created', 'modified',)
