BEGIN;
--
-- Create model Categoria
--
CREATE TABLE "miapp_categoria" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nombre" varchar(100) NOT NULL);
--
-- Create model Cliente
--
CREATE TABLE "miapp_cliente" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nombre" varchar(200) NOT NULL, "email" varchar(254) NOT NULL UNIQUE, "direccion" text NULL);
--
-- Create model Carrito
--
CREATE TABLE "miapp_carrito" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "creado" datetime NOT NULL, "cliente_id" bigint NOT NULL UNIQUE REFERENCES "miapp_cliente" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Producto
--
CREATE TABLE "miapp_producto" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nombre" varchar(200) NOT NULL, "precio" decimal NOT NULL, "imagen" varchar(100) NULL, "categoria_id" bigint NULL REFERENCES "miapp_categoria" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model DetalleCarrito
--
CREATE TABLE "miapp_detallecarrito" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "cantidad" integer unsigned NOT NULL CHECK ("cantidad" >= 0), "carrito_id" bigint NOT NULL REFERENCES "miapp_carrito" ("id") DEFERRABLE INITIALLY DEFERRED, "producto_id" bigint NOT NULL REFERENCES "miapp_producto" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "miapp_producto_categoria_id_365ad5c6" ON "miapp_producto" ("categoria_id");
CREATE UNIQUE INDEX "miapp_detallecarrito_carrito_id_producto_id_cb18f9e1_uniq" ON "miapp_detallecarrito" ("carrito_id", "producto_id");
CREATE INDEX "miapp_detallecarrito_carrito_id_4e54988d" ON "miapp_detallecarrito" ("carrito_id");
CREATE INDEX "miapp_detallecarrito_producto_id_c1806a47" ON "miapp_detallecarrito" ("producto_id");
COMMIT;
