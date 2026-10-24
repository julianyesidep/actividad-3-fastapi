from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4

class ProductoBase(BaseModel):
    nombre: str = Field(
        ...,
        min_length = 2,
        max_length = 100,
        description = "Nombre del producto tecnologico",
        example = "Laptop Gaming RTX 4060"
    )
    precio: float = Field(
        ...,
        gt=0,
        description="Precio Unitarios en COP/USD. Debe ser estrictamente mayor a 0",
        example=4500000.00
    )
    disponible: bool = Field(
        default=True,
        description="Estado de disponibilidad en el inventario"
    )

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_lenght=2, max_length=100)
    precio: Optional[float] = Field(None, gt=0)
    disponible: Optional[bool]= None

class Producto(ProductoBase):
    id: UUID = Field(default_factory=uuid4, description="Identificador Unico Universal (UUIDv4)")

    class Config:
        from_attributes = True