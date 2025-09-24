from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path("", views.home, name="home"),  # esta será la página principal
=======
    path("", views.home, name="home"), 
>>>>>>> ff8b5ed50f4a7397610d007f04f2a189ebe114da
    path("carrito/", views.ver_carrito, name="ver_carrito"),
    path("registrar/", views.registrar_cliente, name="registrar_cliente"),
    path("login/", views.login_cliente, name="login_cliente"),
    path("finalizar-compra/", views.finalizar_compra, name="finalizar_compra"),
    path("agregar/<int:producto_id>/", views.agregar_carrito, name="agregar_carrito"),
]
