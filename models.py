from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Ninja(db.Model):
    __tablename__ = 'ninjas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    rango = db.Column(db.String(20), nullable=False)  # Genin, Chūnin, Jōnin
    ataque = db.Column(db.Integer, default=50)
    defensa = db.Column(db.Integer, default=50)
    chakra = db.Column(db.Integer, default=100)
    aldea = db.Column(db.String(100), default='Konohagakure')
    jutsus = db.Column(db.Text, default='')  # Jutsus separados por comas
    fecha_registro = db.Column(db.DateTime, default=datetime.now)
    
    # Relación con asignaciones
    asignaciones = db.relationship('AsignacionMision', back_populates='ninja', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'rango': self.rango,
            'ataque': self.ataque,
            'defensa': self.defensa,
            'chakra': self.chakra,
            'aldea': self.aldea,
            'jutsus': self.jutsus.split(',') if self.jutsus else [],
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }
    
    def __repr__(self):
        return f'<Ninja {self.nombre} - {self.rango}>'


class Mision(db.Model):
    __tablename__ = 'misiones'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    rango = db.Column(db.String(1), nullable=False)  # D, C, B, A, S
    recompensa = db.Column(db.Integer, default=0)
    descripcion = db.Column(db.Text, default='')
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    
    # Relación con asignaciones
    asignaciones = db.relationship('AsignacionMision', back_populates='mision', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'rango': self.rango,
            'recompensa': self.recompensa,
            'descripcion': self.descripcion,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }
    
    def __repr__(self):
        return f'<Mision {self.nombre} - Rango {self.rango}>'


class AsignacionMision(db.Model):
    __tablename__ = 'asignaciones_misiones'
    
    id = db.Column(db.Integer, primary_key=True)
    ninja_id = db.Column(db.Integer, db.ForeignKey('ninjas.id'), nullable=False)
    mision_id = db.Column(db.Integer, db.ForeignKey('misiones.id'), nullable=False)
    fecha_asignacion = db.Column(db.DateTime, default=datetime.now)
    fecha_completado = db.Column(db.DateTime, nullable=True)
    completada = db.Column(db.Boolean, default=False)
    
    # Relaciones
    ninja = db.relationship('Ninja', back_populates='asignaciones')
    mision = db.relationship('Mision', back_populates='asignaciones')
    
    def to_dict(self):
        return {
            'id': self.id,
            'ninja_id': self.ninja_id,
            'ninja_nombre': self.ninja.nombre if self.ninja else None,
            'mision_id': self.mision_id,
            'mision_nombre': self.mision.nombre if self.mision else None,
            'fecha_asignacion': self.fecha_asignacion.isoformat() if self.fecha_asignacion else None,
            'fecha_completado': self.fecha_completado.isoformat() if self.fecha_completado else None,
            'completada': self.completada
        }
    
    def __repr__(self):
        return f'<AsignacionMision {self.ninja.nombre} -> {self.mision.nombre}>'