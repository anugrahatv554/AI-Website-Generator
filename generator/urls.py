from django.urls import path
from .views import generate_website, index, preview_page

urlpatterns = [
    path('', index, name='index'),
    path('generate/', generate_website, name='generate_website'),
    path('preview/', preview_page, name='preview_page'),
]
