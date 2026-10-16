import sqlite3
import os

# Abrir bd
def conexionDB():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "basedatos.db")
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# Creacion tablas
def crearTablas():
    conn = conexionDB()
    cursor = conn.cursor()
    
    # Tabla clientes
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                rfc TEXT,
                email TEXT,
                telefono TEXT,
                direccion TEXT
            )""")
    # Tabla productos
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                precio_unitario REAL NOT NULL
            )""")
    # Tabla facturas
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS facturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                folio TEXT NOT NULL,
                id_cliente INTEGER NOT NULL,
                fecha_emision TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
                estatus TEXT NOT NULL DEFAULT 'pendiente' CHECK(estatus IN ('pendiente', 'pagado', 'cancelado')),
                notas TEXT,
                FOREIGN KEY (id_cliente) REFERENCES clientes(id)
            )   
            """)
    # Tabla detalles de factura
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS detalle_factura (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_factura INTEGER NOT NULL,
                id_producto INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (id_factura) REFERENCES facturas(id),
                FOREIGN KEY (id_producto) REFERENCES productos(id)
            )
            """)
    conn.commit()
    conn.close()