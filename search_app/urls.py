from django.urls import path
from . import views

urlpatterns = [
    path('', views.doc_search, name='search_documents'),
]