Bienvenido aca le enseñare como funciona mi aplicación en django.

primero tendremos que crear el Entorno Virtual, y, para eso usaremos el siguiente comando.

en windows.

python -m venv venv
venv\Scripts\activate

en linux.

python3 -m venv venv
source venv/bin/activate




Luego instalaremos las dependencias con el siguiente comando.

pip install -r requirements.txt

esto lo que hara es instalar todo lo necesario para que el proyecto funcione.



migraremos la base de datos con el siguiente comando.

python manage.py migrate




se creara un superusuario en caso de que quiera modificar algo en las Bases de Datos.

python manage.py createsuperuser
se ingresara nombre, correo y contraseña (correo opcional)




se levantara el servidor con el siguiente comando.

py manage.py runserver

el proyecto estará disponible en:
http://127.0.0.1:8000/



¿Como funciona mi proyecto?

Este proyecto representa un supermercado creado bajo el nombre Ubicazione.

  Los usuarios pueden agregar productos a su carrito de compras.

  Se puede visualizar el carrito en sesión y el carrito guardado en base de datos.

  Para comprar, el usuario debe registrarse o iniciar sesión.

  Si la sesión ya está creada, al agregar productos se guardan directamente en la base de datos.

  Desde el carrito se puede:

	Finalizar la compra.

	Volver a la página principal.

NOTA
asegurese de tener python 3.10 o superior instalado.