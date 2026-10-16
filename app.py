from flask import Flask, request, jsonify
from db import conexionDB, crearTablas
import re
import sqlite3

app = Flask(__name__, static_folder='static')

# ───────────────────────── COMPROBACIONES ──────────────────────────────

def validate_email(email: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))

# ─────────────────────────────── GET ───────────────────────────────────

# Get clientes
@app.route("/clientes", methods=["GET"])
def obtenerCliente():
    try: 
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")
        datos = cursor.fetchall()
        clientes = []
        for fila in datos:
            clientes.append({
                "id": fila[0],
                "nombre": fila[1],
                "rfc": fila[2],
                "email": fila[3],
                "telefono": fila[4],
                "direccion": fila[5]
            })
        conn.close()
        return jsonify(clientes), 200
    except Exception as e: 
        return jsonify({"error":str(e)}), 500
    
# Get productos
@app.route("/productos", methods=["GET"])
def obtenerProductos():
    try: 
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        datos = cursor.fetchall()
        productos = []
        for fila in datos:
            productos.append({
                "id": fila[0],
                "nombre": fila[1],
                "descripcion": fila[2],
                "precio_unitario": fila[3]
            })
        conn.close()
        return jsonify(productos), 200
    except Exception as e: 
        return jsonify({"error":str(e)}), 500

# Get facturas
@app.route("/facturas", methods=["GET"])
def obtenerFacturas():
    try: 
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM facturas")
        datos = cursor.fetchall()
        facturas = []
        for fila in datos:
            facturas.append({
                "id": fila[0],
                "folio": fila[1],
                "id_cliente": fila[2],
                "fecha_emision": fila[3],
                "estatus": fila[4],
                "notas": fila[5]          
            })
        conn.close()
        return jsonify(facturas), 200
    except Exception as e: 
        return jsonify({"error":str(e)}), 500

# Get detalle_factura
@app.route("/detalle_factura", methods=["GET"])
def obtenerDetalleFactura():
    try: 
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM detalle_factura")
        datos = cursor.fetchall()
        detalle_factura = []
        for fila in datos:
            detalle_factura.append({
                "id": fila[0],
                "id_factura": fila[1],
                "id_producto": fila[2],
                "cantidad": fila[3],
                "precio_unitario": fila[4],
                "subtotal": fila[5]          
            })
        conn.close()
        return jsonify(detalle_factura), 200
    except Exception as e: 
        return jsonify({"error":str(e)}), 500
    
# Get cliente por id
@app.route("/clientes/<int:id_cliente>", methods=["GET"])
def obtenerClientePorId(id_cliente):
    try: 
        conn = conexionDB()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM clientes WHERE id = ?", (id_cliente,)).fetchone()
        if not row:
            conn.close()
            return jsonify({"error": "Cliente no encontrado"}), 404
        conn.close()
        return jsonify({
            "id": row[0],
            "nombre": row[1],
            "rfc": row[2],
            "email": row[3],
            "telefono": row[4],
            "direccion": row[5]
        }), 200
    except Exception as e: 
        return jsonify({"error":str(e)}), 500

# Get factura por id
@app.route("/facturas/<int:id_factura>", methods=["GET"])
def obtenerFacturaPorId(id_factura):
    try: 
        conn = conexionDB()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM facturas WHERE id = ?", (id_factura,)).fetchone()
        if not row:
            conn.close()
            return jsonify({"error": "Factura no encontrada"}), 404
        # Traer el detalle de la factura
        detalle = cursor.execute("SELECT * FROM detalle_factura WHERE id_factura = ?", (id_factura,)).fetchall()
        conn.close()
        return jsonify({
            "id": row[0],
            "folio": row[1],
            "id_cliente": row[2],
            "fecha_emision": row[3],
            "estatus": row[4],
            "notas": row[5],
            "productos": [{
                "id": fila[0],
                "id_producto": fila[2],
                "cantidad": fila[3],
                "precio_unitario": fila[4],
                "subtotal": fila[5]
            } for fila in detalle]
        }), 200
    except Exception as e: 
        return jsonify({"error":str(e)}), 500

# Get producto por id
@app.route("/productos/<int:id_producto>", methods=["GET"])
def obtenerProductoPorId(id_producto):
    try: 
        conn = conexionDB()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,)).fetchone()
        if not row:
            conn.close()
            return jsonify({"error": "Producto no encontrado"}), 404
        conn.close()
        return jsonify({
            "id": row[0],
            "nombre": row[1],
            "descripcion": row[2],
            "precio_unitario": row[3]
        }), 200
    except Exception as e: 
        return jsonify({"error":str(e)}), 500

# ──────────────────────────────── POST ─────────────────────────────────

# POST clientes
@app.route("/clientes", methods=["POST"])
def crearCliente():
    try: 
        # ─── VALIDACIONES ───
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Body JSON requerido"}), 400
        if not data.get("nombre"):
            return jsonify({"error": "nombre es requerido"}), 400
        if data.get("email") and not validate_email(str(data["email"])):
            return jsonify({"error": "Email inválido"}), 400
        
        # ──── EJECUCION ─────
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clientes (nombre, rfc, email, telefono, direccion) VALUES (?,?,?,?,?)", 
                       (data.get("nombre"), data.get("rfc"), data.get("email"), data.get("telefono"), data.get("direccion")))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Cliente agregado", "id": cursor.lastrowid}), 201
    except Exception as e: 
        return jsonify({"error":str(e)}), 500
    
# POST productos
@app.route("/productos", methods=["POST"])
def crearProducto():
    try: 
        # ─── VALIDACIONES ───
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Body JSON requerido"}), 400
        if not data.get("nombre"):
            return jsonify({"error": "Campo requerido: nombre"}), 400
        if not data.get("precio_unitario"):
            return jsonify({"error": "Campo requerido: precio unitario"}), 400
        
        # ──── EJECUCION ─────
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, descripcion, precio_unitario) VALUES (?,?,?)", 
                       (data.get("nombre"), data.get("descripcion"), data.get("precio_unitario")))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Producto agregado", "id": cursor.lastrowid}), 201
    except Exception as e: 
        return jsonify({"error":str(e)}), 500
    
# POST facturas
@app.route("/facturas", methods=["POST"])
def crearFactura():
    try: 
        # ─── VALIDACIONES ───
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Body JSON requerido"}), 400
        for field in ["folio"]:
            if field not in data or not str(data[field]).strip():
                return jsonify({"error": f"Campo requerido: {field}"}), 400
        if not data.get("id_cliente"):
            return jsonify({"error": "Campo requerido: cliente"}), 400

        # ──── EJECUCION ─────
        conn = conexionDB()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM clientes WHERE id = ?", (data.get("id_cliente"),)).fetchone()
        if not row:
            conn.close()
            return jsonify({"error": "Cliente no encontrado"}), 404
        cursor.execute("INSERT INTO facturas (folio, id_cliente, notas) VALUES (?,?,?)", 
                    (data.get("folio"), data.get("id_cliente"), data.get("notas")))
        factura_id = cursor.lastrowid
        for producto in data.get("productos"):
            prod_row = cursor.execute("SELECT precio_unitario FROM productos WHERE id = ?", (producto["id_producto"],)).fetchone()
            if not prod_row:
                conn.close()
                return jsonify({"error": f"Producto {producto['id_producto']} no encontrado"}), 404
            precio_unitario = prod_row[0]
            cursor.execute("INSERT INTO detalle_factura (id_factura, id_producto, cantidad, precio_unitario, subtotal) VALUES (?,?,?,?,?)",
                (factura_id, producto["id_producto"], producto["cantidad"], precio_unitario, precio_unitario * producto["cantidad"]))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Factura agregada", "id": factura_id}), 201
    except Exception as e: 
        return jsonify({"error":str(e)}), 500

# ─────────────────────────────── DELETE ────────────────────────────────

# DELETE clientes
@app.route("/clientes/<int:id_cliente>", methods=["DELETE"])
def eliminar_cliente(id_cliente):
    try:
        conn = conexionDB()
        cursor = conn.cursor()
        # ─── VALIDACIONES ───
        row = cursor.execute("SELECT * FROM clientes WHERE id = ?", (id_cliente,)).fetchone()
        if not row:
            conn.close()
            return jsonify({"error": "Cliente no encontrado"}), 404
        # ──── EJECUCION ─────
        cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Cliente eliminado correctamente", "id": id_cliente}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE productos
@app.route("/productos/<int:id_producto>", methods=["DELETE"])
def eliminar_producto(id_producto):
    try:
        conn = conexionDB()
        cursor = conn.cursor()
        # ─── VALIDACIONES ───
        row = cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,)).fetchone()
        if not row:
            conn.close()
            return jsonify({"error": "Producto no encontrado"}), 404
        # ──── EJECUCION ─────
        cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Producto eliminado correctamente", "id": id_producto}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE facturas
@app.route("/facturas/<int:id_factura>", methods=["DELETE"])
def eliminar_factura(id_factura):
    try:
        conn = conexionDB()
        cursor = conn.cursor()
        # ─── VALIDACIONES ───
        row = cursor.execute("SELECT * FROM facturas WHERE id = ?", (id_factura,)).fetchone()
        if not row:
            conn.close()
            return jsonify({"error": "Factura no encontrada"}), 404
        # ──── EJECUCION ─────
        cursor.execute("DELETE FROM detalle_factura WHERE id_factura = ?", (id_factura,))
        cursor.execute("DELETE FROM facturas WHERE id = ?", (id_factura,))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Factura eliminada correctamente", "id": id_factura}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ──────────────────────────────── PUT ─────────────────────────────────

# PUT clientes
@app.route("/clientes/<int:id_cliente>", methods=["PUT"])
def actualizar_cliente(id_cliente):
    try:
        conn = conexionDB()
        cursor = conn.cursor()
        # ─── VALIDACIONES ───
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Body JSON requerido"}), 400
        if data.get("email") and not validate_email(str(data["email"])):
            return jsonify({"error": "Email inválido"}), 400
        row = cursor.execute("SELECT * FROM clientes WHERE id = ?", (id_cliente,)).fetchone()
        if not row:
            conn.close()
            return jsonify({"error": "Cliente no encontrado"}), 404
        # ── OBTENER DATOS ───
        nombre    = data.get("nombre",    row[1])
        rfc       = data.get("rfc",       row[2])
        email     = data.get("email",     row[3])
        telefono  = data.get("telefono",  row[4])
        direccion = data.get("direccion", row[5])
        # ──── EJECUCION ─────
        cursor.execute(
            "UPDATE clientes SET nombre = ?, rfc = ?, email = ?, telefono = ?, direccion = ? WHERE id = ?",
            (nombre, rfc, email, telefono, direccion, id_cliente)
        )
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Cliente actualizado correctamente", "id": id_cliente}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PUT productos
@app.route("/productos/<int:id_producto>", methods=["PUT"])
def actualizar_producto(id_producto):
    try:
        conn = conexionDB()
        cursor = conn.cursor()
        # ─── VALIDACIONES ───
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Body JSON requerido"}), 400
        row = cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,)).fetchone()
        if not row:
            conn.close()
            return jsonify({"error": "Producto no encontrado"}), 404
        # ── OBTENER DATOS ───
        nombre          = data.get("nombre",          row[1])
        descripcion     = data.get("descripcion",     row[2])
        precio_unitario = data.get("precio_unitario", row[3])
        # ──── EJECUCION ─────
        cursor.execute(
            "UPDATE productos SET nombre = ?, descripcion = ?, precio_unitario = ? WHERE id = ?",
            (nombre, descripcion, precio_unitario, id_producto)
        )
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Producto actualizado correctamente", "id": id_producto}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PUT facturas
@app.route("/facturas/<int:id_factura>", methods=["PUT"])
def actualizar_factura(id_factura):
    try:
        conn = conexionDB()
        cursor = conn.cursor()
        # ─── VALIDACIONES ───
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Body JSON requerido"}), 400
        row = cursor.execute("SELECT * FROM facturas WHERE id = ?", (id_factura,)).fetchone()
        if not row:
            conn.close()
            return jsonify({"error": "Factura no encontrada"}), 404
        # ── OBTENER DATOS ───
        folio         = data.get("folio",         row[1])
        id_cliente    = data.get("id_cliente",    row[2])
        fecha_emision = data.get("fecha_emision", row[3])
        estatus       = data.get("estatus",       row[4])
        notas         = data.get("notas",         row[5])
        # ──── EJECUCION ─────
        cursor.execute(
            "UPDATE facturas SET folio = ?, id_cliente = ?, fecha_emision = ?, estatus = ?, notas = ? WHERE id = ?",
            (folio, id_cliente, fecha_emision, estatus, notas, id_factura)
        )
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Factura actualizada correctamente", "id": id_factura}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Debug
if __name__ == "__main__":
    crearTablas()
    app.run(debug=True)