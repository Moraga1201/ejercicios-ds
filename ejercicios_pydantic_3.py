from typing import Annotated
from pydantic import BaseModel, Field, ValidationError

CoordenadasGPS = Annotated[
    float,
    Field(ge=-90.0, le= 90.0)
]

class Ubicacion(BaseModel):
    longitud: CoordenadasGPS
    latitud: CoordenadasGPS
    etiqueta: str | None = None

# instancia valida
ubicacion_valida = Ubicacion(
    longitud=-68.83,
    latitud=-42.76,
    etiqueta="Trelew"
)

print("Ubicacion Valida:")
print(ubicacion_valida)

# Instancia válida sin etiqueta
ubicacion_sin_etiqueta = Ubicacion(
    longitud=-67.5000,
    latitud=-45.8667
)

print("\nUbicación sin etiqueta:")
print(ubicacion_sin_etiqueta)


# Instancia con coordenadas inválidas
print("\nPrueba con coordenadas inválidas:")

try:
    ubicacion_invalida = Ubicacion(
        longitud=-100.0,
        latitud=120.0,
        etiqueta="Ubicación inválida"
    )

    print(ubicacion_invalida)

except ValidationError as error:
    print(error)