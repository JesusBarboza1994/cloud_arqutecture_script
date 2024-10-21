from faker import Faker
import mysql.connector
import random

# Configura Faker
fake = Faker()

# Conectar a la base de datos MySQL
connection = mysql.connector.connect(
    host='db',  # Nombre del servicio definido en Docker Compose
    user='root',
    password='rootpassword',
    database='testdb'
)

cursor = connection.cursor()

# Crear tabla de proveedores si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Proveedor (
        id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
        tipo_documento VARCHAR(50) NOT NULL,
        nro_documento VARCHAR(50) NOT NULL,
        razon_social VARCHAR(255),
        nombre VARCHAR(255),
        apellido_pa VARCHAR(255),
        apellido_ma VARCHAR(255),
        banco VARCHAR(255),
        cuenta VARCHAR(255),
        cci VARCHAR(255),
        direccion VARCHAR(255)
    );
''')

# Verificar si la tabla Proveedor está vacía
cursor.execute("SELECT COUNT(*) FROM Proveedor;")
proveedores_count = cursor.fetchone()[0]

# Insertar proveedores si la tabla está vacía
if proveedores_count == 0:
    for _ in range(100):
        cursor.execute('''
            INSERT INTO Proveedor (tipo_documento, nro_documento, razon_social, nombre, apellido_pa, apellido_ma, banco, cuenta, cci, direccion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            fake.random_element(elements=('DNI', 'RUC')),
            fake.unique.random_number(digits=8),
            fake.company(),
            fake.first_name(),
            fake.last_name(),
            fake.last_name(),
            fake.bank_country(),
            fake.iban(),
            fake.iban(),
            fake.address()
        ))
    print("Se insertaron proveedores.")
else:
    print("La tabla Proveedor ya tiene datos.")

# Crear tabla de productos si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Producto (
        cod_producto INT AUTO_INCREMENT PRIMARY KEY,
        nombre_producto VARCHAR(255) NOT NULL,
        unidad_medida VARCHAR(50),
        cantidad_unidad_medida DECIMAL(10,2),
        stock_actual INT,
        stock_minimo INT,
        stock_maximo INT,
        precio_unitario DECIMAL(10,2),
        tipo_moneda VARCHAR(10),
        fecha_actualizacion DATE
    );
''')

# Verificar si la tabla Producto está vacía
cursor.execute("SELECT COUNT(*) FROM Producto;")
productos_count = cursor.fetchone()[0]

# Insertar 1000 productos si la tabla está vacía
if productos_count == 0:
    for _ in range(1000):
        cursor.execute('''
            INSERT INTO Producto (nombre_producto, unidad_medida, cantidad_unidad_medida, stock_actual, stock_minimo, stock_maximo, precio_unitario, tipo_moneda, fecha_actualizacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            fake.word(),
            fake.random_element(elements=('kg', 'unidad', 'litro')),
            fake.pydecimal(left_digits=3, right_digits=2, positive=True),
            fake.random_int(min=100, max=1000),
            fake.random_int(min=10, max=100),
            fake.random_int(min=1000, max=1500),
            fake.pydecimal(left_digits=4, right_digits=2, positive=True),
            'PEN',
            fake.date_this_year()
        ))
    print("Se insertaron productos.")
else:
    print("La tabla Producto ya tiene datos.")

# Crear tabla de clientes si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cliente (
        id_cliente INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        apellido_pa VARCHAR(255) NOT NULL,
        apellido_ma VARCHAR(255) NOT NULL,
        direccion VARCHAR(255),
        tipo_documento VARCHAR(50),
        nro_documento VARCHAR(50),
        correo VARCHAR(255)
    );
''')

# Verificar si la tabla Cliente está vacía
cursor.execute("SELECT COUNT(*) FROM Cliente;")
clientes_count = cursor.fetchone()[0]

# Insertar 2000 clientes si la tabla está vacía
if clientes_count == 0:
    for _ in range(2000):
        cursor.execute('''
            INSERT INTO Cliente (nombre, apellido_pa, apellido_ma, direccion, tipo_documento, nro_documento, correo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            fake.first_name(),
            fake.last_name(),
            fake.last_name(),
            fake.address(),
            fake.random_element(elements=('DNI', 'RUC', 'PASAPORTE')),
            fake.unique.random_number(digits=8),
            fake.email()
        ))
    print("Se insertaron clientes.")
else:
    print("La tabla Cliente ya tiene datos.")

# Crear tabla de movimientos de productos si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Movimiento_producto (
        id_movimiento INT AUTO_INCREMENT PRIMARY KEY,
        fecha_registro DATE,
        hora_registro TIME,
        cod_producto INT,
        tipo_moneda VARCHAR(10),
        tipo_cambio DECIMAL(10,2),
        id_detalle_compra INT,
        monto_compra DECIMAL(10,2),
        id_venta INT,
        monto_venta DECIMAL(10,2),
        cantidad INT,
        clase VARCHAR(50),
        FOREIGN KEY (cod_producto) REFERENCES Producto(cod_producto)
    );
''')

# Obtener IDs de productos, clientes y proveedores existentes
cursor.execute("SELECT id_proveedor FROM Proveedor;")
proveedores_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT cod_producto FROM Producto;")
productos_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id_cliente FROM Cliente;")
clientes_ids = [row[0] for row in cursor.fetchall()]

# Crear tabla de Compras si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Compra (
        id_compra INT AUTO_INCREMENT PRIMARY KEY,
        id_proveedor INT,
        cod_compra VARCHAR(50),
        fecha_registro DATE,
        hora_registro TIME,
        usuario_registrador VARCHAR(255),
        tipo_moneda VARCHAR(10),
        tipo_cambio DECIMAL(10,2),
        tipo_documento VARCHAR(50),
        num_documento VARCHAR(50),
        fecha_documento DATE,
        total_subtotal_compra DECIMAL(10,2),
        total_igv_compra DECIMAL(10,2),
        total_monto_compra DECIMAL(10,2),
        status VARCHAR(50),
        FOREIGN KEY (id_proveedor) REFERENCES Proveedor(id_proveedor)
    );
''')

# Crear tabla de Detalle de compra si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Detalle_compra (
        id_compra INT,
        cod_producto INT,
        cantidad_compra INT,
        subtotal_compra DECIMAL(10,2),
        igv_compra DECIMAL(10,2),
        monto_compra DECIMAL(10,2),
        PRIMARY KEY (id_compra, cod_producto),
        FOREIGN KEY (id_compra) REFERENCES Compra(id_compra),
        FOREIGN KEY (cod_producto) REFERENCES Producto(cod_producto)
    );
''')

### 1. Crear Compras y Detalle_compra
for _ in range(10):  # Simulamos 10 compras
    id_proveedor = fake.random_element(proveedores_ids)
    total_subtotal_compra = 0
    total_igv_compra = 0
    total_monto_compra = 0

    # Insertar compra
    cursor.execute('''
        INSERT INTO Compra (id_proveedor, cod_compra, fecha_registro, hora_registro, usuario_registrador, tipo_moneda, tipo_cambio, total_subtotal_compra, total_igv_compra, total_monto_compra, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        id_proveedor,
        fake.unique.random_number(digits=8),
        fake.date_this_year(),
        fake.time(),
        fake.name(),
        'PEN',
        round(random.uniform(1.0, 4.0), 2),
        0, 0, 0,  # Inicializamos con 0 porque vamos a acumular después
        fake.random_element(elements=('completado', 'pendiente'))
    ))
    id_compra = cursor.lastrowid  # Obtener el ID de la compra recién creada

    num_detalles = fake.random_int(1, 10)  # Número aleatorio de detalles de compra
    for _ in range(num_detalles):
        cod_producto = fake.random_element(productos_ids)
        cantidad_compra = fake.random_int(min=1, max=100)
        subtotal_compra = round(cantidad_compra * random.uniform(5.0, 20.0), 2)
        igv_compra = round(subtotal_compra * 0.18, 2)  # IGV del 18%
        monto_compra = round(subtotal_compra + igv_compra, 2)

        # Insertar en Detalle_compra
        cursor.execute('''
            INSERT INTO Detalle_compra (id_compra, cod_producto, cantidad_compra, subtotal_compra, igv_compra, monto_compra)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (
            id_compra,
            cod_producto,
            cantidad_compra,
            subtotal_compra,
            igv_compra,
            monto_compra
        ))

        # Acumular en los totales de la compra
        total_subtotal_compra += subtotal_compra
        total_igv_compra += igv_compra
        total_monto_compra += monto_compra

        # Insertar en Movimiento_producto (ingreso al stock)
        cursor.execute('''
            INSERT INTO Movimiento_producto (fecha_registro, hora_registro, cod_producto, tipo_moneda, tipo_cambio, id_detalle_compra, monto_compra, cantidad, clase)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            fake.date_this_year(),
            fake.time(),
            cod_producto,
            'PEN',
            round(random.uniform(1.0, 4.0), 2),
            id_compra,
            monto_compra,
            cantidad_compra,
            'ingreso'
        ))

    # Actualizar los totales en la tabla Compra
    cursor.execute('''
        UPDATE Compra
        SET total_subtotal_compra = %s, total_igv_compra = %s, total_monto_compra = %s
        WHERE id_compra = %s
    ''', (
        total_subtotal_compra,
        total_igv_compra,
        total_monto_compra,
        id_compra
    ))

# Crear tabla de Ventas si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Venta (
        id_venta INT AUTO_INCREMENT PRIMARY KEY,
        cod_venta VARCHAR(50),
        id_cliente INT,
        fecha_registro DATE,
        hora_registro TIME,
        usuario_registrador VARCHAR(255),
        tipo_moneda VARCHAR(10),
        tipo_cambio DECIMAL(10,2),
        comprobante_pago VARCHAR(50),
        comprobante_numero VARCHAR(50),
        total_subtotal_venta DECIMAL(10,2),
        total_igv_venta DECIMAL(10,2),
        total_monto_venta DECIMAL(10,2),
        metodo_pago VARCHAR(50),
        monto_recibido DECIMAL(10,2),
        vuelto DECIMAL(10,2),
        status VARCHAR(50),
        FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
    );
''')

# Crear tabla de Detalle de venta si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Detalle_venta (
        id_venta INT,
        cod_producto INT,
        cantidad_venta INT,
        subtotal_venta DECIMAL(10,2),
        igv_venta DECIMAL(10,2),
        monto_venta DECIMAL(10,2),
        PRIMARY KEY (id_venta, cod_producto),
        FOREIGN KEY (id_venta) REFERENCES Venta(id_venta),
        FOREIGN KEY (cod_producto) REFERENCES Producto(cod_producto)
    );
''')

### 2. Crear Ventas y Detalle_venta
for _ in range(10):  # Simulamos 10 ventas
    id_cliente = fake.random_element(clientes_ids)
    total_subtotal_venta = 0
    total_igv_venta = 0
    total_monto_venta = 0

    # Insertar venta
    cursor.execute('''
        INSERT INTO Venta (id_cliente, cod_venta, fecha_registro, hora_registro, usuario_registrador, tipo_moneda, tipo_cambio, total_subtotal_venta, total_igv_venta, total_monto_venta, metodo_pago, monto_recibido, vuelto, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        id_cliente,
        fake.unique.random_number(digits=8),
        fake.date_this_year(),
        fake.time(),
        fake.name(),
        'PEN',
        round(random.uniform(1.0, 4.0), 2),
        0, 0, 0,  # Inicializamos con 0 porque vamos a acumular después
        fake.random_element(elements=('Efectivo', 'Tarjeta', 'Transferencia')),
        0, 0,  # Inicializamos para monto_recibido y vuelto
        fake.random_element(elements=('completado', 'pendiente'))
    ))
    id_venta = cursor.lastrowid  # Obtener el ID de la venta recién creada

    num_detalles = fake.random_int(1, 10)  # Número aleatorio de detalles de venta
    for _ in range(num_detalles):
        cod_producto = fake.random_element(productos_ids)
        cantidad_venta = fake.random_int(min=1, max=10)
        subtotal_venta = round(cantidad_venta * random.uniform(5.0, 20.0), 2)
        igv_venta = round(subtotal_venta * 0.18, 2)  # IGV del 18%
        monto_venta = round(subtotal_venta + igv_venta, 2)

        # Insertar en Detalle_venta
        cursor.execute('''
            INSERT INTO Detalle_venta (id_venta, cod_producto, cantidad_venta, subtotal_venta, igv_venta, monto_venta)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (
            id_venta,
            cod_producto,
            cantidad_venta,
            subtotal_venta,
            igv_venta,
            monto_venta
        ))

        # Acumular en los totales de la venta
        total_subtotal_venta += subtotal_venta
        total_igv_venta += igv_venta
        total_monto_venta += monto_venta

        # Insertar en Movimiento_producto (egreso del stock)
        cursor.execute('''
            INSERT INTO Movimiento_producto (fecha_registro, hora_registro, cod_producto, tipo_moneda, tipo_cambio, id_venta, monto_venta, cantidad, clase)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            fake.date_this_year(),
            fake.time(),
            cod_producto,
            'PEN',
            round(random.uniform(1.0, 4.0), 2),
            id_venta,
            monto_venta,
            cantidad_venta,
            'egreso'
        ))

    # Actualizar los totales en la tabla Venta
    cursor.execute('''
        UPDATE Venta
        SET total_subtotal_venta = %s, total_igv_venta = %s, total_monto_venta = %s
        WHERE id_venta = %s
    ''', (
        total_subtotal_venta,
        total_igv_venta,
        total_monto_venta,
        id_venta
    ))


# Guardar los cambios
connection.commit()

# Cerrar la conexión
cursor.close()
connection.close()
