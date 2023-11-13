from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.forms import VersionForm, ProductForm
from catalog.models import Product, Category, Version
from pytils.translit import slugify


class IndexView(TemplateView):
    template_name = 'catalog/index.html'
    extra_context = {'title': '@: Главная'}

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Product.objects.all()
        return context_data


class CategoryListView(ListView):
    extra_context = {'title': '@: Cписок категорий'}
    model = Category


class ProductListView(ListView):
    extra_context = {'title': '@: Каталог обьявлений'}
    model = Product

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True, category_id=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        category_item = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data['category_pk'] = category_item.pk,
        context_data['title'] = f'@: Все обьявления категории {category_item.name}'

        for data in context_data['product_list']:
            active_version = Version.objects.filter(product=data, current_version_indicator=True).last()
            if active_version:
                data.active_version_number = active_version.version_number
            else:
                data.active_version_number = None

        return context_data


class ProductDetailView(LoginRequiredMixin, DetailView):
    extra_context = {'title': '@: Каталог обьявлений'}
    model = Product

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        if form.is_valid():
            new_obj = form.save()
            new_obj.slug = slugify(new_obj.name)
            new_obj.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(
            category_id=self.kwargs.get('pk'),
            owner=self.request.user
        )

    def get_success_url(self):
        return reverse('catalog:detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        return super().get_form_class()

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)

        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object, )
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        if form.is_valid():
            new_obj = form.save()
            new_obj.slug = slugify(new_obj.name)
            new_obj.save()
            self.object.save()
            formset = self.get_context_data()['formset']
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(
            category_id=self.kwargs.get('pk'),
            owner=self.request.user
        )


class ContactsTemplateView(TemplateView):
    template_name = 'catalog/contacts.html'
    extra_context = {'title': '@: Контакты'}
