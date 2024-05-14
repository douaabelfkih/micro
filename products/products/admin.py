from django.contrib import admin
from .models import Product


class productadmin(admin.ModelAdmin):
    list_display = ("name", "slug", "price", "stock", "description","thumbnail")



admin.site.register(Product, productadmin)