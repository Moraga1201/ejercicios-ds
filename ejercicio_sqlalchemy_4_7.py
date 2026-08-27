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
    __tablename__ = "departamentos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]

    profesores: Mapped[list["Profesor"]] = relationship(
        back_populates="departamento"
    )


class Profesor(Base):
    __tablename__ = "profesores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    fecha_ingreso: Mapped[datetime]

    departamento_id: Mapped[int] = mapped_column(
        ForeignKey("departamentos.id")
    )

    departamento: Mapped["Departamento"] = relationship(
        back_populates="profesores"
    )

    # un profesor puede dictar muchos cursos
    cursos: Mapped[list["Curso"]] = relationship(
        back_populates="profesor"
    )


class Curso(Base):
    __tablename__ = "cursos"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str]
    creditos: Mapped[int]

    profesor_id: Mapped[int] = mapped_column(
        ForeignKey("profesores.id")
    )

    profesor: Mapped["Profesor"] = relationship(
        back_populates="cursos"
    )

    
    clases: Mapped[list["Clase"]] = relationship(
        back_populates="curso"
    )

   
    inscripciones: Mapped[list["Inscripcion"]] = relationship(
        back_populates="curso"
    )



class Clase(Base):
    __tablename__ = "clases"

    id: Mapped[int] = mapped_column(primary_key=True)
    tema: Mapped[str]
    duracion_minutos: Mapped[int]

    curso_id: Mapped[int] = mapped_column(
        ForeignKey("cursos.id")
    )

    curso: Mapped["Curso"] = relationship(
        back_populates="clases"
    )




class Estudiante(Base):
    __tablename__ = "estudiantes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    legajo: Mapped[str] = mapped_column(unique=True)

    inscripciones: Mapped[list["Inscripcion"]] = relationship(
        back_populates="estudiante"
    )



class Inscripcion(Base):
    __tablename__ = "inscripciones"

    estudiante_id: Mapped[int] = mapped_column(
        ForeignKey("estudiantes.id"),
        primary_key=True
    )

    curso_id: Mapped[int] = mapped_column(
        ForeignKey("cursos.id"),
        primary_key=True
    )

    fecha_inscripcion: Mapped[datetime]

    calificacion_final: Mapped[float | None] = mapped_column(
        nullable=True
    )

    estudiante: Mapped["Estudiante"] = relationship(
        back_populates="inscripciones"
    )

    curso: Mapped["Curso"] = relationship(
        back_populates="inscripciones"
    )



engine = create_engine(
    "sqlite:///universidad.db",
    echo=True
)

Base.metadata.create_all(engine)


with Session(engine) as session:
    
    departamento_existente = session.scalars(
        select(Departamento)
    ).first()

    if departamento_existente is None:
        departamento_informatica = Departamento(
            nombre="Informática"
        )

        profesor_1 = Profesor(
            nombre="Carlos Gómez",
            email="carlos@gmail.com",
            fecha_ingreso=datetime.now(),
            departamento=departamento_informatica
        )

        profesor_2 = Profesor(
            nombre="Ana López",
            email="ana@gmail.com",
            fecha_ingreso=datetime.now(),
            departamento=departamento_informatica
        )

        profesor_3 = Profesor(
            nombre="María Rodríguez",
            email="maria@gmail.com",
            fecha_ingreso=datetime.now(),
            departamento=departamento_informatica
        )

    
        curso_python = Curso(
            titulo="Programación con Python",
            creditos=6,
            profesor=profesor_1
        )

        curso_bd = Curso(
            titulo="Bases de Datos",
            creditos=5,
            profesor=profesor_1
        )

        curso_sqlalchemy = Curso(
            titulo="SQLAlchemy",
            creditos=4,
            profesor=profesor_2
        )

     
        clase_1 = Clase(
            tema="Variables y tipos de datos",
            duracion_minutos=90,
            curso=curso_python
        )

        clase_2 = Clase(
            tema="Funciones en Python",
            duracion_minutos=120,
            curso=curso_python
        )

        clase_3 = Clase(
            tema="Modelo relacional",
            duracion_minutos=90,
            curso=curso_bd
        )

        clase_4 = Clase(
            tema="Consultas SQL",
            duracion_minutos=120,
            curso=curso_bd
        )

        clase_5 = Clase(
            tema="Introducción a SQLAlchemy",
            duracion_minutos=90,
            curso=curso_sqlalchemy
        )

        clase_6 = Clase(
            tema="Relaciones entre modelos",
            duracion_minutos=120,
            curso=curso_sqlalchemy
        )


        estudiante_1 = Estudiante(
            nombre="Juan Pérez",
            legajo="A001"
        )

        estudiante_2 = Estudiante(
            nombre="Lucía Fernández",
            legajo="A002"
        )

        estudiante_3 = Estudiante(
            nombre="Laura Martínez",
            legajo="A003"
        )


        inscripcion_1 = Inscripcion(
            estudiante=estudiante_1,
            curso=curso_python,
            fecha_inscripcion=datetime.now(),
            calificacion_final=8.0
        )

        inscripcion_2 = Inscripcion(
            estudiante=estudiante_1,
            curso=curso_bd,
            fecha_inscripcion=datetime.now(),
            calificacion_final=7.0
        )

        inscripcion_3 = Inscripcion(
            estudiante=estudiante_2,
            curso=curso_python,
            fecha_inscripcion=datetime.now(),
            calificacion_final=9.0
        )

        inscripcion_4 = Inscripcion(
            estudiante=estudiante_2,
            curso=curso_sqlalchemy,
            fecha_inscripcion=datetime.now(),
            calificacion_final=None
        )

        inscripcion_5 = Inscripcion(
            estudiante=estudiante_3,
            curso=curso_bd,
            fecha_inscripcion=datetime.now(),
            calificacion_final=10.0
        )

        session.add(departamento_informatica)
        session.commit()

        print("\nLos datos se insertaron correctamente.")

    else:
        print("\nLos datos ya estaban registrados.")



with Session(engine) as session:
    profesores = session.scalars(
        select(Profesor)
    ).all()

    print("\n========================================")
    print("EJERCICIO 4: CURSOS POR PROFESOR")
    print("========================================")

    for profesor in profesores:
        print(f"\nProfesor: {profesor.nombre}")

        if profesor.cursos:
            for curso in profesor.cursos:
                print(
                    f"- Curso: {curso.titulo} | "
                    f"Créditos: {curso.creditos}"
                )
        else:
            print("- No tiene cursos asignados")




with Session(engine) as session:
    curso = session.scalars(
        select(Curso).where(
            Curso.titulo == "Programación con Python"
        )
    ).first()


    print(": CLASES DE UN CURSO")


    if curso:
        print(f"\nCurso: {curso.titulo}")

        for clase in curso.clases:
            print(
                f"- Tema: {clase.tema} | "
                f"Duración: {clase.duracion_minutos} minutos"
            )
    else:
        print("No se encontró el curso.")


with Session(engine) as session:
    estudiantes = session.scalars(
        select(Estudiante)
    ).all()

    print(" INSCRIPCIONES")


    for estudiante in estudiantes:
        print(
            f"\nEstudiante: {estudiante.nombre} | "
            f"Legajo: {estudiante.legajo}"
        )

        for inscripcion in estudiante.inscripciones:
            if inscripcion.calificacion_final is None:
                calificacion = "Sin calificación"
            else:
                calificacion = str(
                    inscripcion.calificacion_final
                )

            print(
                f"- Curso: {inscripcion.curso.titulo} | "
                f"Fecha: {inscripcion.fecha_inscripcion} | "
                f"Calificación final: {calificacion}"
            )