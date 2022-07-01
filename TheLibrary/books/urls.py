# Django
from django.urls import path

from books import views

urlpatterns = [
    
    path('', views.ListCreateBooksAPIView.as_view(), name='get_post_book'),
    path('<int:pk>', views.RetrieveUpdateDestroyBooksAPIView.as_view(), name='get_delete_update_book'),

]
