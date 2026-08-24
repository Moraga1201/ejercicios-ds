from typing import Literal
from pydantic import BaseModel, ValidationError

class Dispositivo(BaseModel):
    id_dispositivo: int | str
    tipo: Literal["sensor", "actuador", "gateway"]

# primera instancia identificar entero

dispositivo_1 = Dispositivo(
    id_dispositivo=1001,
    tipo = "sensor"
)

print("Primer dispositivo:")
print(dispositivo_1)

# segunda instancia identificador de tipo string

dispositivo_2 = Dispositivo(
    id_dispositivo="DISP-2002",
    tipo="gateway"
)

print("\nSegundo Dispositivo:")
print(dispositivo_2)

print("\nPrueba con un tipo invalido:")

try:
    dispositivo_invalido = Dispositivo(
        id_dispositivo=3003,
        tipo="camara"
    )

    print(dispositivo_invalido)

except ValidationError as Error:
    print(error)