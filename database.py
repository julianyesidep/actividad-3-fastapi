from typing import List
from models import Producto
from uuid import uuid4

db_productos: List[Producto] = []

def cargar_datos_semilla():
    if not db_productos:
        db_productos.extend([
            Producto(
                id=uuid4(),
                nombre="Laptop Asus ROG Strix",
                precio=5200000.0,
                disponible=True
            ),
            Producto(
                id=uuid4(),
                nombre="Mouse Inalámbrico Logitech MX Master 35",
                precio=480000.0,
                disponible=True
            ),
            Producto(
                id=uuid4(),
                nombre="Teclado Mecánico Keychron K2 V2",
                precio=390000.0,
                disponible=True
            )
        ])