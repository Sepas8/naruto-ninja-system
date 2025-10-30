from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from models import db, Ninja, Mision, AsignacionMision
from datetime import datetime
import os


class ConfiguracionApp:
    """Clase para gestionar la configuración de la aplicación"""
    
    def __init__(self):
        self.DATABASE_URL = os.getenv(
            'DATABASE_URL', 
            'postgresql://naruto_user:konoha123@db:5432/naruto_db'
        )
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.DEBUG = True
        self.HOST = '0.0.0.0'
        self.PORT = 5000


class ValidadorRangos:
    """Clase para validar rangos de ninjas y misiones"""
    
    RANGOS_NINJA = ['Genin', 'Chūnin', 'Jōnin']
    RANGOS_MISION = ['D', 'C', 'B', 'A', 'S']
    
    JERARQUIA_NINJA = {'Genin': 1, 'Chūnin': 2, 'Jōnin': 3}
    JERARQUIA_MISION = {'D': 1, 'C': 1, 'B': 2, 'A': 3, 'S': 3}
    
    @classmethod
    def validar_rango_ninja(cls, rango):
        """Valida si el rango de ninja es válido"""
        return rango in cls.RANGOS_NINJA
    
    @classmethod
    def validar_rango_mision(cls, rango):
        """Valida si el rango de misión es válido"""
        return rango in cls.RANGOS_MISION
    
    @classmethod
    def puede_realizar_mision(cls, rango_ninja, rango_mision):
        """Verifica si un ninja puede realizar una misión según su rango"""
        jerarquia_n = cls.JERARQUIA_NINJA.get(rango_ninja, 0)
        jerarquia_m = cls.JERARQUIA_MISION.get(rango_mision, 0)
        return jerarquia_n >= jerarquia_m


class NinjaController:
    """Controlador para gestionar operaciones de Ninjas"""
    
    def __init__(self):
        self.validador = ValidadorRangos()
    
    def listar_todos(self):
        """Obtiene todos los ninjas"""
        try:
            ninjas = Ninja.query.all()
            return {'success': True, 'data': [ninja.to_dict() for ninja in ninjas]}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def obtener_por_id(self, ninja_id):
        """Obtiene un ninja por su ID"""
        try:
            ninja = Ninja.query.get_or_404(ninja_id)
            return {'success': True, 'data': ninja.to_dict()}
        except Exception as e:
            return {'success': False, 'error': 'Ninja no encontrado'}
    
    def crear(self, datos):
        """Crea un nuevo ninja"""
        try:
            # Validar rango
            if not self.validador.validar_rango_ninja(datos.get('rango')):
                return {
                    'success': False, 
                    'error': f'Rango inválido. Debe ser uno de: {ValidadorRangos.RANGOS_NINJA}'
                }
            
            ninja = Ninja(
                nombre=datos['nombre'],
                rango=datos['rango'],
                ataque=datos.get('ataque', 50),
                defensa=datos.get('defensa', 50),
                chakra=datos.get('chakra', 100),
                aldea=datos.get('aldea', 'Konohagakure'),
                jutsus=datos.get('jutsus', '')
            )
            
            db.session.add(ninja)
            db.session.commit()
            
            return {'success': True, 'data': ninja.to_dict(), 'message': 'Ninja creado correctamente'}
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def actualizar(self, ninja_id, datos):
        """Actualiza un ninja existente"""
        try:
            ninja = Ninja.query.get_or_404(ninja_id)
            
            if 'nombre' in datos:
                ninja.nombre = datos['nombre']
            if 'rango' in datos:
                if self.validador.validar_rango_ninja(datos['rango']):
                    ninja.rango = datos['rango']
            if 'ataque' in datos:
                ninja.ataque = datos['ataque']
            if 'defensa' in datos:
                ninja.defensa = datos['defensa']
            if 'chakra' in datos:
                ninja.chakra = datos['chakra']
            if 'aldea' in datos:
                ninja.aldea = datos['aldea']
            if 'jutsus' in datos:
                ninja.jutsus = datos['jutsus']
            
            db.session.commit()
            return {'success': True, 'data': ninja.to_dict(), 'message': 'Ninja actualizado'}
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def eliminar(self, ninja_id):
        """Elimina un ninja"""
        try:
            ninja = Ninja.query.get_or_404(ninja_id)
            db.session.delete(ninja)
            db.session.commit()
            return {'success': True, 'message': 'Ninja eliminado correctamente'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}


class MisionController:
    """Controlador para gestionar operaciones de Misiones"""
    
    def __init__(self):
        self.validador = ValidadorRangos()
    
    def listar_todas(self):
        """Obtiene todas las misiones"""
        try:
            misiones = Mision.query.all()
            return {'success': True, 'data': [mision.to_dict() for mision in misiones]}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def obtener_por_id(self, mision_id):
        """Obtiene una misión por su ID"""
        try:
            mision = Mision.query.get_or_404(mision_id)
            return {'success': True, 'data': mision.to_dict()}
        except Exception as e:
            return {'success': False, 'error': 'Misión no encontrada'}
    
    def crear(self, datos):
        """Crea una nueva misión"""
        try:
            # Validar rango
            if not self.validador.validar_rango_mision(datos.get('rango')):
                return {
                    'success': False,
                    'error': f'Rango inválido. Debe ser uno de: {ValidadorRangos.RANGOS_MISION}'
                }
            
            mision = Mision(
                nombre=datos['nombre'],
                rango=datos['rango'],
                recompensa=datos.get('recompensa', 0),
                descripcion=datos.get('descripcion', '')
            )
            
            db.session.add(mision)
            db.session.commit()
            
            return {'success': True, 'data': mision.to_dict(), 'message': 'Misión creada correctamente'}
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def eliminar(self, mision_id):
        """Elimina una misión"""
        try:
            mision = Mision.query.get_or_404(mision_id)
            db.session.delete(mision)
            db.session.commit()
            return {'success': True, 'message': 'Misión eliminada correctamente'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}


class AsignacionController:
    """Controlador para gestionar asignaciones de misiones"""
    
    def __init__(self):
        self.validador = ValidadorRangos()
    
    def listar_todas(self):
        """Obtiene todas las asignaciones"""
        try:
            asignaciones = AsignacionMision.query.all()
            return {'success': True, 'data': [asig.to_dict() for asig in asignaciones]}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def crear(self, datos):
        """Asigna una misión a un ninja"""
        try:
            ninja = Ninja.query.get_or_404(datos['ninja_id'])
            mision = Mision.query.get_or_404(datos['mision_id'])
            
            # Validar compatibilidad de rangos
            if not self.validador.puede_realizar_mision(ninja.rango, mision.rango):
                return {
                    'success': False,
                    'error': f'{ninja.nombre} (rango {ninja.rango}) no tiene el rango suficiente para la misión {mision.rango}'
                }
            
            asignacion = AsignacionMision(
                ninja_id=ninja.id,
                mision_id=mision.id,
                fecha_asignacion=datetime.now(),
                completada=False
            )
            
            db.session.add(asignacion)
            db.session.commit()
            
            return {'success': True, 'data': asignacion.to_dict(), 'message': 'Misión asignada correctamente'}
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def completar(self, asignacion_id):
        """Marca una asignación como completada"""
        try:
            asignacion = AsignacionMision.query.get_or_404(asignacion_id)
            asignacion.completada = True
            asignacion.fecha_completado = datetime.now()
            db.session.commit()
            
            return {'success': True, 'data': asignacion.to_dict(), 'message': 'Misión completada'}
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}


class ReporteController:
    """Controlador para generar reportes y estadísticas"""
    
    def generar_reporte_ninjas(self):
        """Genera reporte detallado de ninjas"""
        try:
            ninjas = Ninja.query.all()
            reporte = []
            
            for ninja in ninjas:
                misiones_asignadas = AsignacionMision.query.filter_by(ninja_id=ninja.id).count()
                misiones_completadas = AsignacionMision.query.filter_by(
                    ninja_id=ninja.id, 
                    completada=True
                ).count()
                
                reporte.append({
                    'ninja': ninja.to_dict(),
                    'misiones_asignadas': misiones_asignadas,
                    'misiones_completadas': misiones_completadas,
                    'tasa_completado': round(
                        (misiones_completadas / misiones_asignadas * 100) if misiones_asignadas > 0 else 0,
                        2
                    )
                })
            
            return {'success': True, 'data': reporte}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def generar_reporte_misiones(self):
        """Genera reporte detallado de misiones"""
        try:
            misiones = Mision.query.all()
            reporte = []
            
            for mision in misiones:
                asignaciones = AsignacionMision.query.filter_by(mision_id=mision.id).all()
                ninjas_asignados = [asig.ninja.nombre for asig in asignaciones]
                completada = any(asig.completada for asig in asignaciones)
                
                reporte.append({
                    'mision': mision.to_dict(),
                    'ninjas_asignados': ninjas_asignados,
                    'total_asignaciones': len(asignaciones),
                    'completada': completada
                })
            
            return {'success': True, 'data': reporte}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}


class AplicacionNaruto:
    """Clase principal de la aplicación - Arquitectura Monolítica Orientada a Objetos"""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.config = ConfiguracionApp()
        self.ninja_controller = NinjaController()
        self.mision_controller = MisionController()
        self.asignacion_controller = AsignacionController()
        self.reporte_controller = ReporteController()
        
        self._configurar_app()
        self._configurar_base_datos()
        self._registrar_rutas()
    
    def _configurar_app(self):
        """Configura la aplicación Flask"""
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.config.DATABASE_URL
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = self.config.SQLALCHEMY_TRACK_MODIFICATIONS
        CORS(self.app)
    
    def _configurar_base_datos(self):
        """Inicializa la base de datos"""
        db.init_app(self.app)
        
        with self.app.app_context():
            db.create_all()
    
    def _registrar_rutas(self):
        """Registra todas las rutas de la aplicación"""
        
        # Ruta principal
        @self.app.route('/')
        def index():
            return render_template('index.html')
        
        # Servir archivos estáticos desde pagina/
        @self.app.route('/pagina/<path:path>')
        def send_pagina(path):
            return send_from_directory('pagina', path)
        
        # === RUTAS NINJAS ===
        @self.app.route('/api/ninjas', methods=['GET'])
        def listar_ninjas():
            resultado = self.ninja_controller.listar_todos()
            if resultado['success']:
                return jsonify(resultado['data']), 200
            return jsonify({'error': resultado['error']}), 400
        
        @self.app.route('/api/ninjas/<int:id>', methods=['GET'])
        def consultar_ninja(id):
            resultado = self.ninja_controller.obtener_por_id(id)
            if resultado['success']:
                return jsonify(resultado['data']), 200
            return jsonify({'error': resultado['error']}), 404
        
        @self.app.route('/api/ninjas', methods=['POST'])
        def registrar_ninja():
            resultado = self.ninja_controller.crear(request.json)
            if resultado['success']:
                return jsonify(resultado['data']), 201
            return jsonify({'error': resultado['error']}), 400
        
        @self.app.route('/api/ninjas/<int:id>', methods=['PUT'])
        def actualizar_ninja(id):
            resultado = self.ninja_controller.actualizar(id, request.json)
            if resultado['success']:
                return jsonify(resultado['data']), 200
            return jsonify({'error': resultado['error']}), 400
        
        @self.app.route('/api/ninjas/<int:id>', methods=['DELETE'])
        def eliminar_ninja(id):
            resultado = self.ninja_controller.eliminar(id)
            if resultado['success']:
                return jsonify({'mensaje': resultado['message']}), 200
            return jsonify({'error': resultado['error']}), 400
        
        # === RUTAS MISIONES ===
        @self.app.route('/api/misiones', methods=['GET'])
        def listar_misiones():
            resultado = self.mision_controller.listar_todas()
            if resultado['success']:
                return jsonify(resultado['data']), 200
            return jsonify({'error': resultado['error']}), 400
        
        @self.app.route('/api/misiones/<int:id>', methods=['GET'])
        def consultar_mision(id):
            resultado = self.mision_controller.obtener_por_id(id)
            if resultado['success']:
                return jsonify(resultado['data']), 200
            return jsonify({'error': resultado['error']}), 404
        
        @self.app.route('/api/misiones', methods=['POST'])
        def registrar_mision():
            resultado = self.mision_controller.crear(request.json)
            if resultado['success']:
                return jsonify(resultado['data']), 201
            return jsonify({'error': resultado['error']}), 400
        
        @self.app.route('/api/misiones/<int:id>', methods=['DELETE'])
        def eliminar_mision(id):
            resultado = self.mision_controller.eliminar(id)
            if resultado['success']:
                return jsonify({'mensaje': resultado['message']}), 200
            return jsonify({'error': resultado['error']}), 400
        
        # === RUTAS ASIGNACIONES ===
        @self.app.route('/api/asignaciones', methods=['GET'])
        def listar_asignaciones():
            resultado = self.asignacion_controller.listar_todas()
            if resultado['success']:
                return jsonify(resultado['data']), 200
            return jsonify({'error': resultado['error']}), 400
        
        @self.app.route('/api/asignaciones', methods=['POST'])
        def asignar_mision():
            resultado = self.asignacion_controller.crear(request.json)
            if resultado['success']:
                return jsonify(resultado['data']), 201
            return jsonify({'error': resultado['error']}), 400
        
        @self.app.route('/api/asignaciones/<int:id>/completar', methods=['PUT'])
        def completar_mision(id):
            resultado = self.asignacion_controller.completar(id)
            if resultado['success']:
                return jsonify(resultado['data']), 200
            return jsonify({'error': resultado['error']}), 400
        
        # === RUTAS REPORTES ===
        @self.app.route('/api/reportes/ninjas', methods=['GET'])
        def reporte_ninjas():
            resultado = self.reporte_controller.generar_reporte_ninjas()
            if resultado['success']:
                return jsonify(resultado['data']), 200
            return jsonify({'error': resultado['error']}), 400
        
        @self.app.route('/api/reportes/misiones', methods=['GET'])
        def reporte_misiones():
            resultado = self.reporte_controller.generar_reporte_misiones()
            if resultado['success']:
                return jsonify(resultado['data']), 200
            return jsonify({'error': resultado['error']}), 400
    
    def ejecutar(self):
        """Inicia la aplicación"""
        self.app.run(
            host=self.config.HOST,
            port=self.config.PORT,
            debug=self.config.DEBUG
        )


# Punto de entrada de la aplicación
if __name__ == '__main__':
    aplicacion = AplicacionNaruto()
    aplicacion.ejecutar()