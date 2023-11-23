from django.urls import path
from catalog.views import IndexView, ProductCreateView, ProductListView, ContactsTemplateView, CategoryListView, \
    ProductDetailView, ProductUpdateView, ProductDeleteView
from catalog.apps import CatalogConfig
from django.views.decorators.cache import cache_page

app_name = CatalogConfig.name

urlpatterns = [
    path('', cache_page(420)(IndexView.as_view()), name='index'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('catalog/update/<int:pk>/', ProductUpdateView.as_view(), name='update'),
    path('catalog/delete/<int:pk>', ProductDeleteView.as_view(), name='delete'),
    path('contacts/', cache_page(420)(ContactsTemplateView.as_view()), name='contacts'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('catalog/<int:pk>', ProductDetailView.as_view(), name='detail'),
    path('category/<int:pk>', ProductListView.as_view(), name='category_objects'),
]
