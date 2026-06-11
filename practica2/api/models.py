from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)

    preguntas = relationship("Pregunta", back_populates="categoria")


class Pregunta(Base):
    __tablename__ = "preguntas"

    id = Column(Integer, primary_key=True, index=True)
    pregunta = Column(Text, nullable=False)
    respuesta = Column(Text, nullable=False)
    activa = Column(Boolean, default=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)
    keyw = Column(Text, nullable=True)

    categoria = relationship("Categoria", back_populates="preguntas")
    logs = relationship("Log", back_populates="pregunta")


class UsuarioAdmin(Base):
    __tablename__ = "usuarios_admin"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)


class Config(Base):
    __tablename__ = "config"

    id = Column(Integer, primary_key=True, index=True)
    clave = Column(String(100), nullable=False, unique=True)
    valor = Column(Text, nullable=True)


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    usuario_telegram = Column(String(100), nullable=True)
    consulta = Column(Text, nullable=False)
    respuesta = Column(Text, nullable=True)
    pregunta_id = Column(Integer, ForeignKey("preguntas.id"), nullable=True)

    pregunta = relationship("Pregunta", back_populates="logs")
