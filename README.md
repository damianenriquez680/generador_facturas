# Generador de facturas

API REST con Flask + SQLite para gestionar clientes, productos y facturas.
Frontend en HTML/CSS/JS vanilla y generación de PDF con WeasyPrint en desarrollo.

> Proyecto personal
> Iniciado: Septiembre 2026
> Estado: En curso ⚒️

---

## Estado del proyecto

- [x] Base de datos SQLite (4 tablas)
- [x] API REST completa (GET, POST, PUT, DELETE)
- [x] Probado con Postman
- [ ] Frontend en HTML/CSS/JS
- [ ] Generación de facturas en PDF (WeasyPrint)

---

## Instalación rápida

```bash
pip install flask
python app.py
# API en: http://127.0.0.1:5000
```

---

## Estructura

```
├── app.py          # API Flask (rutas y validaciones)
├── db.py           # Conexión y creación de tablas
├── basedatos.db    # Base de datos SQLite (se genera sola)
├── templates/      # HTML (en desarrollo)
└── static/         # CSS y JS (en desarrollo)
```

---

## Base de datos

| Tabla | Descripción |
|-------|-------------|
| `clientes` | Nombre, RFC, email, teléfono y dirección |
| `productos` | Nombre, descripción y precio unitario |
| `facturas` | Folio, cliente, fecha, estatus (`pendiente`, `pagado`, `cancelado`) y notas |
| `detalle_factura` | Productos de cada factura con cantidad, precio y subtotal |

La fecha de emisión (hora local) y el estatus se asignan automáticamente con `DEFAULT`.
El precio y el subtotal de cada línea se calculan en el servidor a partir del producto.

---

## Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /clientes, /productos, /facturas | Listar |
| GET | /detalle_factura | Listar todas las líneas de detalle |
| GET | /clientes/:id, /productos/:id | Obtener uno |
| GET | /facturas/:id | Obtener una factura con su detalle de productos |
| POST | /clientes, /productos | Crear |
| POST | /facturas | Crear factura con sus productos |
| PUT | /clientes/:id, /productos/:id, /facturas/:id | Actualizar (solo los campos enviados) |
| DELETE | /clientes/:id, /productos/:id | Eliminar |
| DELETE | /facturas/:id | Eliminar factura y su detalle |

---

## Ejemplo de uso

```bash
# Crear factura
curl -X POST http://localhost:5000/facturas \
  -H "Content-Type: application/json" \
  -d '{"folio":"FAC-002","id_cliente":1,"notas":"Prueba","productos":[{"id_producto":1,"cantidad":2}]}'
```

---

## Buenas prácticas aplicadas

- Placeholders `?` en todas las consultas SQL (previene inyección SQL)
- Validación de campos requeridos antes de operar
- Validación de formato de email
- Manejo de errores con `try/except` y códigos HTTP (400, 404, 500)
- Código separado: conexión y tablas en `db.py`, rutas en `app.py`