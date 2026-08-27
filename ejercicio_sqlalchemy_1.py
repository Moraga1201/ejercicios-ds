from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

class Base(DeclarativeBase):
    pass

class Profesor(Base):
    __tablename__= "profesores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    email: Mapped[str]
    fecha_ingreso: Mapped[datetime]

engine = create_engine(
    "sqlite:///universidad.db",
    echo=True
)

Base.metadata.create_all(engine)

with Session(engine) as session:
    profesor_1 = Profesor(
        nombre="Carlos Gomez",
        email="carlos@gmail.com",
        fecha_ingreso=datetime.now()
    )

    profesor_2 = Profesor(
        nombre="Ana Lopez",
        email="Ana@gmail.com",
        fecha_ingreso=datetime.now()
    )

    session.add_all([profesor_1, profesor_2])
    session.commit()

with Session(engine) as session:
    consulta = select(Profesor)
    profesores = session.scalars(consulta).all()

    print("\n Profesores Registrados:")

    for profesor in profesores:
        print(
            f"ID: {profesor.id} | "
            f"Nombre: {profesor.nombre} | "
            f"Email: {profesor.email} | "
            f"Fecha de ingreso: {profesor.fecha_ingreso}"
        )