from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from blog.models import Post


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(published=True)
        return queryset


class PostCreateView(CreateView):
    model = Post
    fields = ('name', 'content', 'image', 'published')
    success_url = reverse_lazy('blog:post_list', )


class PostDetailView(DetailView):
    model = Post

    def get_object(self, **kwargs):
        views = super().get_object()
        views.increase_view_count()
        return views


class PostUpdateView(UpdateView):
    model = Post
    fields = ('name', 'slug', 'content', 'image', 'published')

    def get_success_url(self):
        return reverse('blog:post_item', kwargs={'slug': self.object.slug})


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')
