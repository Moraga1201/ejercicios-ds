from pydantic import BaseModel, EmailStr, Field, ValidationError

class Estudiante(BaseModel):
    legajo: int = Field(gt=0)
    nombre_completo: str = Field(min_length=5)
    email: EmailStr
    promedio: float = Field(default=0.0, ge=0.0, le=10.0)

# instancia correcta

estudiante_valido = Estudiante(
    legajo=1234,
    nombre_completo="Lautaro Moraga",
    email="lautaro@gmail.com",
    promedio=8.5
)

print("Estudiante valido:")
print(estudiante_valido)

# datos para provocar posibles errores

casos_invalidos = [
    (
        "legajo no positivo",
        {
            "legajo": 0,
            "nombre_completo": "Lautaro Moraga",
            "email": "lautaro@gmail.com",
            "promedio": 8.5
        }
    ),
    (
        "Nombre demasiado corto",
        {
            "legajo": 1234,
            "nombre_completo": "Ana",
            "email": "ana@gmail.com",
            "promedio": 8.5
        }
    ),
    (
        "Correo electrónico inválido",
        {
            "legajo": 1234,
            "nombre_completo": "Lautaro Moraga",
            "email": "correo-invalido",
            "promedio": 8.5
        }
    ),
    (
        "Promedio menor que cero",
        {
            "legajo": 1234,
            "nombre_completo": "Lautaro Moraga",
            "email": "lautaro@gmail.com",
            "promedio": -1
        }
    ),
    (
        "Promedio mayor que diez",
        {
            "legajo": 1234,
            "nombre_completo": "Lautaro Moraga",
            "email": "lautaro@gmail.com",
            "promedio": 11
        }
    )
]

for descripcion, datos in casos_invalidos:
    print(f"\n --- Prueba: {descripcion} ---")

    try:
        estudiante = Estudiante(**datos)
        print(estudiante)

    except ValidationError as error:
        print(error)