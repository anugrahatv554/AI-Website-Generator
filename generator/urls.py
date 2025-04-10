from django.urls import path
from .views import generate_website, index, preview_page

urlpatterns = [
    # path('generate/', generate_website),
    # path('preview/<str:site_id>/', preview_site),
    path('', index, name='index'),
    # path('preview/', preview_page, name='preview_page'),
    path('generate/', generate_website, name='generate_website'),
    path('preview/', preview_page, name='preview_page'),
]
