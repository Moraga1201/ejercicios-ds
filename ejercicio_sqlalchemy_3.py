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

    # Relación desde Departamento hacia Profesor
    profesores: Mapped[list["Profesor"]] = relationship(
        back_populates="departamento"
    )


class Profesor(Base):
    __tablename__ = "profesores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    email: Mapped[str]
    fecha_ingreso: Mapped[datetime]

    departamento_id: Mapped[int] = mapped_column(
        ForeignKey("departamento.id")
    )

    # Relación desde Profesor hacia Departamento
    departamento: Mapped["Departamento"] = relationship(
        back_populates="profesores"
    )


engine = create_engine(
    "sqlite:///universidad.db",
    echo=True
)

Base.metadata.create_all(engine)


# Insertar un departamento con tres profesores
with Session(engine) as session:
    departamento_ingenieria = Departamento(
        nombre="Ingeniería"
    )

    profesor_1 = Profesor(
        nombre="Carlos Gómez",
        email="carlos@gmail.com",
        fecha_ingreso=datetime.now()
    )

    profesor_2 = Profesor(
        nombre="Ana López",
        email="ana@gmail.com",
        fecha_ingreso=datetime.now()
    )

    profesor_3 = Profesor(
        nombre="María Rodríguez",
        email="maria@gmail.com",
        fecha_ingreso=datetime.now()
    )

    departamento_ingenieria.profesores.extend(
        [profesor_1, profesor_2, profesor_3]
    )

    session.add(departamento_ingenieria)
    session.commit()


# Verificar la navegación en ambos sentidos
with Session(engine) as session:
    consulta = select(Departamento).where(
        Departamento.nombre == "Ingeniería"
    )

    departamento = session.scalars(consulta).first()

    if departamento:
        print("\nNavegación desde Departamento hacia Profesores")
        print(f"Departamento: {departamento.nombre}")

        for profesor in departamento.profesores:
            print(f"- Profesor: {profesor.nombre}")

        print("\nNavegación desde Profesor hacia Departamento")

        for profesor in departamento.profesores:
            print(
                f"- {profesor.nombre} pertenece al departamento "
                f"{profesor.departamento.nombre}"
            )