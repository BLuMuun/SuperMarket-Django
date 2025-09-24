from django.contrib import admin
from .models import Categoria, Producto, Cliente, Carrito, DetalleCarrito


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "categoria")
    search_fields = ("nombre",)
    list_filter = ("categoria",)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email", "direccion")
    search_fields = ("nombre", "email")


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "creado")
    search_fields = ("cliente__nombre",)
    list_filter = ("creado",)


@admin.register(DetalleCarrito)
class DetalleCarritoAdmin(admin.ModelAdmin):
    list_display = ("carrito", "producto", "cantidad")
    search_fields = ("producto__nombre", "carrito__cliente__nombre")
