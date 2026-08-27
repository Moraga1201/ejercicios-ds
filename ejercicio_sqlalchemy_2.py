from datetime import datetime

from sqlalchemy import ForeignKey, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


class Departamento(Base):
    __tablename__ = "departamento"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]

    profesores: Mapped[list["Profesor"]] = relationship()


class Profesor(Base):
    __tablename__ = "profesores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    email: Mapped[str]
    fecha_ingreso: Mapped[datetime]

    departamento_id: Mapped[int] = mapped_column(
        ForeignKey("departamento.id")
    )


engine = create_engine(
    "sqlite:///universidad.db",
    echo=True
)

Base.metadata.create_all(engine)


with Session(engine) as session:
    departamento_informatica = Departamento(
        nombre="Informática"
    )

    profesor_1 = Profesor(
        nombre="Carlos Gómez",
        email="carlos@gmail.com",
        fecha_ingreso=datetime.now()
    )

    profesor_2 = Profesor(
        nombre="Ana López",
        email="anaL@gmail.com",
        fecha_ingreso=datetime.now()
    )

    departamento_informatica.profesores.append(profesor_1)
    departamento_informatica.profesores.append(profesor_2)

    session.add(departamento_informatica)
    session.commit()


with Session(engine) as session:
    consulta = select(Departamento)
    departamentos = session.scalars(consulta).all()

    print("\nDEPARTAMENTOS Y PROFESORES")

    for departamento in departamentos:
        print(f"\nDepartamento: {departamento.nombre}")

        for profesor in departamento.profesores:
            print(
                f"- ID: {profesor.id} | "
                f"Nombre: {profesor.nombre} | "
                f"Email: {profesor.email} | "
                f"Departamento ID: {profesor.departamento_id}"
            )