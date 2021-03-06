# Generated by Django 4.0.5 on 2022-07-04 03:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authors',
            options={'ordering': ('fullname',), 'permissions': (('view_all_authors', 'Can view all authors'),), 'verbose_name': 'Autor', 'verbose_name_plural': 'Autores'},
        ),
        migrations.RemoveField(
            model_name='authors',
            name='lastname',
        ),
        migrations.RemoveField(
            model_name='authors',
            name='name',
        ),
        migrations.AddField(
            model_name='authors',
            name='fullname',
            field=models.CharField(default='', max_length=50, verbose_name='Nombre(s)'),
        ),
        migrations.AlterField(
            model_name='books',
            name='books_register',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='book_editor', to=settings.AUTH_USER_MODEL, verbose_name='Registrado por'),
        ),
        migrations.AlterField(
            model_name='books',
            name='subtitle',
            field=models.CharField(default='', max_length=50, verbose_name='Sub-Titulo'),
        ),
    ]
