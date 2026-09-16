from django.urls import path

from catalog.apps import CatalogConfig

from . import views


app_name = CatalogConfig.name

urlpatterns = [
    path("", views.ProductListView.as_view(), name="home"),
    path(
        "products/<int:pk>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
]