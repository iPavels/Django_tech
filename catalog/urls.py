from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home, contacts
from . import views

app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name='home'),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path('contacts/',contacts, name='contacts'),
]