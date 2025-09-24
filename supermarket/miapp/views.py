from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages
from .models import Producto, Categoria, Cliente, Carrito, DetalleCarrito


def home(request):
    """Página principal con lista de productos y categorías."""
    query = request.GET.get("q")
    categoria_id = request.GET.get("categoria")

    productos = Producto.objects.all()
    if query:
        productos = productos.filter(nombre__icontains=query)
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    categorias = Categoria.objects.all()
    return render(request, "index.html", {
        "productos": productos,
        "categorias": categorias
    })


@transaction.atomic
def finalizar_compra(request):
    """Vaciar el carrito en BD después de la compra."""
    if "cliente_id" not in request.session:
        messages.error(request, "Debes iniciar sesión para finalizar la compra.")
        return redirect("registrar_cliente")

    cliente = Cliente.objects.filter(id=request.session["cliente_id"]).first()
    if not cliente:
        messages.error(request, "Cliente no encontrado.")
        return redirect("registrar_cliente")

    carrito = Carrito.objects.filter(cliente=cliente).first()
    if not carrito:
        messages.error(request, "Tu carrito está vacío.")
        return redirect("ver_carrito")

    carrito.detalles.all().delete()

    messages.success(request, "¡Compra finalizada con éxito! Tu carrito fue vaciado.")
    return redirect("ver_carrito")


def _ensure_single_carrito(cliente):
    """Devuelve un único carrito para el cliente, consolida si hay varios."""
    qs = list(Carrito.objects.filter(cliente=cliente).order_by("id"))
    if not qs:
        return Carrito.objects.create(cliente=cliente)
    if len(qs) == 1:
        return qs[0]

    principal = qs[0]
    extras = qs[1:]
    for extra in extras:
        for d in list(extra.detalles.all()):
            dp = DetalleCarrito.objects.filter(carrito=principal, producto=d.producto).first()
            if dp:
                dp.cantidad += d.cantidad
                dp.save()
            else:
                d.carrito = principal
                d.save()
        extra.delete()
    return principal


@transaction.atomic
def registrar_cliente(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        direccion = request.POST.get("direccion")

        cliente, created = Cliente.objects.get_or_create(
            email=email,
            defaults={"nombre": nombre, "direccion": direccion}
        )
        if not created:
            cliente.nombre = nombre
            cliente.direccion = direccion
            cliente.save()

        request.session["cliente_id"] = cliente.id

        carrito = _ensure_single_carrito(cliente)
        session_cart = request.session.get("carrito", {})
        for item in session_cart.values():
            try:
                producto = Producto.objects.get(id=item["id"])
            except Producto.DoesNotExist:
                continue
            detalle, creado = DetalleCarrito.objects.get_or_create(
                carrito=carrito,
                producto=producto,
                defaults={"cantidad": int(item.get("cantidad", 1))}
            )
            if not creado:
                detalle.cantidad += int(item.get("cantidad", 1))
                detalle.save()

        request.session["carrito"] = {}
        request.session.modified = True

        messages.success(request, "Cliente registrado y carrito guardado en BD.")
        return redirect("ver_carrito")

    return render(request, "registrar_cliente.html")


def login_cliente(request):
    if request.method == "POST":
        email = request.POST.get("email")
        cliente = Cliente.objects.filter(email=email).first()
        if not cliente:
            messages.error(request, "Cliente no encontrado.")
            return render(request, "registrar_cliente.html", {"error": "Cliente no encontrado"})

        request.session["cliente_id"] = cliente.id

        session_cart = request.session.get("carrito", {})
        if session_cart:
            carrito = _ensure_single_carrito(cliente)
            for item in session_cart.values():
                try:
                    producto = Producto.objects.get(id=item["id"])
                except Producto.DoesNotExist:
                    continue
                detalle, creado = DetalleCarrito.objects.get_or_create(
                    carrito=carrito,
                    producto=producto,
                    defaults={"cantidad": int(item.get("cantidad", 1))}
                )
                if not creado:
                    detalle.cantidad += int(item.get("cantidad", 1))
                    detalle.save()

            request.session["carrito"] = {}
            request.session.modified = True

        messages.success(request, "Inicio de sesión correcto. Carrito guardado en BD.")
        return redirect("ver_carrito")

    return redirect("registrar_cliente")


@transaction.atomic
def agregar_carrito(request, producto_id):
    if request.method != "POST":
        return redirect("home")

    producto = get_object_or_404(Producto, id=producto_id)

    if "cliente_id" not in request.session:
        session_cart = request.session.get("carrito", {})
        key = str(producto_id)
        if key in session_cart:
            session_cart[key]["cantidad"] += 1
        else:
            session_cart[key] = {
                "id": producto.id,
                "nombre": producto.nombre,
                "precio": float(producto.precio),
                "cantidad": 1,
            }
        request.session["carrito"] = session_cart
        request.session.modified = True
        messages.success(request, f"'{producto.nombre}' agregado al carrito (sesión).")
        return redirect("ver_carrito")

    cliente = Cliente.objects.filter(id=request.session.get("cliente_id")).first()
    if not cliente:
        messages.error(request, "Cliente inválido en sesión. Inicia sesión de nuevo.")
        return redirect("registrar_cliente")

    carrito = _ensure_single_carrito(cliente)
    detalle, created = DetalleCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    if created:
        detalle.cantidad = 1
    else:
        detalle.cantidad += 1
    detalle.save()

    messages.success(request, f"'{producto.nombre}' agregado al carrito.")
    return redirect("ver_carrito")


def ver_carrito(request):
    """Mostrar carrito de sesión y de BD (si hay cliente logueado)."""
    carrito_items = []
    total = 0.0

    session_cart = request.session.get("carrito", {})
    for item in session_cart.values():
        subtotal = float(item["precio"]) * int(item["cantidad"])
        carrito_items.append({
            "nombre": item["nombre"],
            "cantidad": item["cantidad"],
            "subtotal": subtotal
        })
        total += subtotal

    cliente = None
    carrito_bd = None
    detalles_data = []
    total_bd = 0.0

    if "cliente_id" in request.session:
        cliente = Cliente.objects.filter(id=request.session["cliente_id"]).first()
        if cliente:
            carrito_bd = _ensure_single_carrito(cliente)
            detalles = carrito_bd.detalles.select_related("producto").all()
            for d in detalles:
                precio = float(d.producto.precio or 0)
                cantidad = int(d.cantidad or 0)
                subtotal = precio * cantidad
                detalles_data.append({
                    "producto": d.producto,
                    "cantidad": cantidad,
                    "subtotal": subtotal
                })
                total_bd += subtotal

    return render(request, "carrito.html", {
        "cliente": cliente,
        "carrito_items": carrito_items,
        "total": total,
        "carrito_bd": carrito_bd,
        "detalles": detalles_data,
        "total_bd": total_bd,
    })
