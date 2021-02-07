from django.contrib import admin

# Register your models here.
from .models import Category, Product, View

class admin_Category(admin.ModelAdmin):
    list_display = ('str_nombre', 'created_at','updated_at')

class admin_Product(admin.ModelAdmin):
    list_display = ('str_sku', 'str_name', 'str_price', 'obj_categoria' ,'created_at','updated_at')

class admin_View(admin.ModelAdmin):
    list_display = ('obj_products', 'str_times','created_at','updated_at')

admin.site.register(Category, admin_Category)
admin.site.register(Product, admin_Product)
admin.site.register(View, admin_View)
