from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    template_name = "blog/blogpost_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog/blogpost_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        post.views_count += 1
        post.save(update_fields=["views_count"])
        return post


class BlogPostCreateView(CreateView):
    model = BlogPost
    template_name = "blog/blogpost_form.html"
    fields = [
        "title",
        "content",
        "preview",
        "is_published",
    ]
    success_url = reverse_lazy("blog:list")


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    template_name = "blog/blogpost_form.html"
    fields = [
        "title",
        "content",
        "preview",
        "is_published",
    ]

    def get_success_url(self):
        return self.object.get_absolute_url()


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = "blog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("blog:list")