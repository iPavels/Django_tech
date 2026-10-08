from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import ProductForm
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset()

        # Модератор видит все продукты.
        if self.request.user.has_perm("catalog.delete_product"):
            return queryset

        # Авторизованный пользователь видит опубликованные
        # продукты и свои продукты.
        if self.request.user.is_authenticated:
            return queryset.filter(
                Q(is_published=True) | Q(owner=self.request.user)
            )

        # Неавторизованный пользователь видит
        # только опубликованные продукты.
        return queryset.filter(is_published=True)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_queryset(self):
        queryset = super().get_queryset()

        # Модератор может редактировать любой продукт.
        if self.request.user.has_perm("catalog.delete_product"):
            return queryset

        # Обычный пользователь может редактировать
        # только свои продукты.
        return queryset.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse(
            "catalog:product_detail",
            kwargs={"pk": self.object.pk},
        )


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")

    def get_queryset(self):
        queryset = super().get_queryset()

        # Модератор может удалить любой продукт.
        if self.request.user.has_perm("catalog.delete_product"):
            return queryset

        # Обычный пользователь может удалить
        # только свой продукт.
        return queryset.filter(owner=self.request.user)


class ProductUnpublishView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    View,
):
    permission_required = "catalog.can_unpublish_product"

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        product.is_published = False
        product.save(update_fields=["is_published"])

        return redirect(
            "catalog:product_detail",
            pk=product.pk,
        )