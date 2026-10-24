from fastapi import FastAPI, HTTPException, status
from typing import List
from uuid import UUID

from models import Producto,ProductoCreate, ProductoUpdate
from database import db_productos, cargar_datos_semilla

app =  FastAPI(
    title = "API Catálogo de Porductos Efímero - SENA ADSO",
    description="API RESTful para la gestion de inventarios tecnológicos en memoria utilizadno Pydantic y FastAPI.",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    cargar_datos_semilla()

@app.get(
    "/",
    tags=["Raíz"],
    summary="Mensaje de Bienvenida"
)
def welcome():
    return{
        "mensaje": "Bienvenido a la API del Catálogo de Productos Efímerio (SENA ADSO)",
        "documentacion": "/docs"
    }


@app.get(
    "/productos",
    response_model=List[Producto],
    status_code=status.HTTP_200_OK,
    tags=["Productos"],
    summary="Obtener todo el inventario"
)
def get_productos():
    return db_productos

@app.get(
    "/productos/{producto_id}",
    response_model=Producto,
    status_code=status.HTTP_200_OK,
    tags=["Productos"],
    summary="Buscar producto por ID"
)
def get_producto_por_id(producto_id: UUID):
    for prod in db_productos:
        if prod.id == producto_id:
            return prod

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"EL producto con ID '{producto_id}' no fue encontrado en el catálogo."
    )

@app.post(
    "/productos",
    response_model=Producto,
    status_code=status.HTTP_201_CREATED,
    tags=["Productos"],
    summary="Agregar nuevo producto"
)
def create_producto(producto_in: ProductoCreate):
    for prod in db_productos:
        if prod.nombre.lower() == producto_in.nombre.lower():
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un producto registrado con el nombre '{producto_in.nombre}'."
            )
    
    nuevo_producto = Producto(**producto_in.model_dump())
    db_productos.append(nuevo_producto)
    return nuevo_producto

@app.put(
    "/productos/{producto_id}",
    response_model=Producto,
    status_code=status.HTTP_200_OK,
    tags=["Productos"],
    summary="Actualizar producto por ID"
)

def update_producto(producto_id: UUID,producto_update:ProductoUpdate):
    for index, prod in enumerate(db_productos):
        if prod.id == producto_id:
            datos_actualizados = producto_update.model_dump(exclude_unset=True)

            producto_modificado = prod.model_copy(update=datos_actualizados)
            db_productos[index] = producto_modificado
            return producto_modificado

    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No es posible actualizar. El producto con ID '{producto_id}' no existe."
        )

@app.delete(
    "/productos/{producto_id}",
    status_code=status.HTTP_200_OK,
    tags=["Productos"],
    summary="Eliminar producto por ID"
)

def delete_producto(producto_id: UUID):
    for index, prod in enumerate(db_productos):
        if prod.id == producto_id:
            producto_eliminado = db_productos.pop(index)
            return{
                "mensaje": "Producto eliminado exitosamente",
                "producto_eliminado": producto_eliminado
            }

    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No es posible eliminar. El producto con ID '{producto_id}' no existe."
        )