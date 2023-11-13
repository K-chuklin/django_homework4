from django.contrib import admin
from catalog.models import Product, Category, Version
from users.models import User


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description',)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'version_number', 'name_version', 'current_version_indicator')
    list_filter = ('version_number',)
    search_fields = ('version_number', 'name_version',)


admin.site.register(User)
