from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from models import db, Ninja, Mision, AsignacionMision
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://naruto_user:konoha123@db:5432/naruto_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Crear tablas al iniciar
with app.app_context():
    db.create_all()

# ============== RUTAS DEL CLIENTE WEB ==============
@app.route('/')
def index():
    return render_template('index.html')

# ============== API REST - NINJAS ==============
@app.route('/api/ninjas', methods=['GET'])
def listar_ninjas():
    ninjas = Ninja.query.all()
    return jsonify([ninja.to_dict() for ninja in ninjas])

@app.route('/api/ninjas/<int:id>', methods=['GET'])
def consultar_ninja(id):
    ninja = Ninja.query.get_or_404(id)
    return jsonify(ninja.to_dict())

@app.route('/api/ninjas', methods=['POST'])
def registrar_ninja():
    data = request.json
    
    # Validaciones
    rangos_validos = ['Genin', 'Chūnin', 'Jōnin']
    if data.get('rango') not in rangos_validos:
        return jsonify({'error': f'Rango inválido. Debe ser uno de: {rangos_validos}'}), 400
    
    try:
        ninja = Ninja(
            nombre=data['nombre'],
            rango=data['rango'],
            ataque=data.get('ataque', 50),
            defensa=data.get('defensa', 50),
            chakra=data.get('chakra', 100),
            aldea=data.get('aldea', 'Konohagakure'),
            jutsus=data.get('jutsus', '')
        )
        db.session.add(ninja)
        db.session.commit()
        return jsonify(ninja.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/ninjas/<int:id>', methods=['PUT'])
def actualizar_ninja(id):
    ninja = Ninja.query.get_or_404(id)
    data = request.json
    
    if 'nombre' in data:
        ninja.nombre = data['nombre']
    if 'rango' in data:
        ninja.rango = data['rango']
    if 'ataque' in data:
        ninja.ataque = data['ataque']
    if 'defensa' in data:
        ninja.defensa = data['defensa']
    if 'chakra' in data:
        ninja.chakra = data['chakra']
    if 'aldea' in data:
        ninja.aldea = data['aldea']
    if 'jutsus' in data:
        ninja.jutsus = data['jutsus']
    
    db.session.commit()
    return jsonify(ninja.to_dict())

@app.route('/api/ninjas/<int:id>', methods=['DELETE'])
def eliminar_ninja(id):
    ninja = Ninja.query.get_or_404(id)
    db.session.delete(ninja)
    db.session.commit()
    return jsonify({'mensaje': 'Ninja eliminado correctamente'}), 200

# ============== API REST - MISIONES ==============
@app.route('/api/misiones', methods=['GET'])
def listar_misiones():
    misiones = Mision.query.all()
    return jsonify([mision.to_dict() for mision in misiones])

@app.route('/api/misiones/<int:id>', methods=['GET'])
def consultar_mision(id):
    mision = Mision.query.get_or_404(id)
    return jsonify(mision.to_dict())

@app.route('/api/misiones', methods=['POST'])
def registrar_mision():
    data = request.json
    
    # Validaciones
    rangos_validos = ['D', 'C', 'B', 'A', 'S']
    if data.get('rango') not in rangos_validos:
        return jsonify({'error': f'Rango inválido. Debe ser uno de: {rangos_validos}'}), 400
    
    try:
        mision = Mision(
            nombre=data['nombre'],
            rango=data['rango'],
            recompensa=data.get('recompensa', 0),
            descripcion=data.get('descripcion', '')
        )
        db.session.add(mision)
        db.session.commit()
        return jsonify(mision.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/misiones/<int:id>', methods=['DELETE'])
def eliminar_mision(id):
    mision = Mision.query.get_or_404(id)
    db.session.delete(mision)
    db.session.commit()
    return jsonify({'mensaje': 'Misión eliminada correctamente'}), 200

# ============== API REST - ASIGNACIÓN DE MISIONES ==============
@app.route('/api/asignaciones', methods=['GET'])
def listar_asignaciones():
    asignaciones = AsignacionMision.query.all()
    return jsonify([asig.to_dict() for asig in asignaciones])

@app.route('/api/asignaciones', methods=['POST'])
def asignar_mision():
    data = request.json
    
    ninja = Ninja.query.get_or_404(data['ninja_id'])
    mision = Mision.query.get_or_404(data['mision_id'])
    
    # Validar rango del ninja
    jerarquia_ninja = {'Genin': 1, 'Chūnin': 2, 'Jōnin': 3}
    jerarquia_mision = {'D': 1, 'C': 1, 'B': 2, 'A': 3, 'S': 3}
    
    if jerarquia_ninja.get(ninja.rango, 0) < jerarquia_mision.get(mision.rango, 0):
        return jsonify({
            'error': f'{ninja.nombre} (rango {ninja.rango}) no tiene el rango suficiente para la misión {mision.rango}'
        }), 400
    
    try:
        asignacion = AsignacionMision(
            ninja_id=ninja.id,
            mision_id=mision.id,
            fecha_asignacion=datetime.now(),
            completada=False
        )
        db.session.add(asignacion)
        db.session.commit()
        return jsonify(asignacion.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/asignaciones/<int:id>/completar', methods=['PUT'])
def completar_mision(id):
    asignacion = AsignacionMision.query.get_or_404(id)
    asignacion.completada = True
    asignacion.fecha_completado = datetime.now()
    db.session.commit()
    return jsonify(asignacion.to_dict())

# ============== REPORTES ==============
@app.route('/api/reportes/ninjas', methods=['GET'])
def reporte_ninjas():
    ninjas = Ninja.query.all()
    reporte = []
    
    for ninja in ninjas:
        misiones_asignadas = AsignacionMision.query.filter_by(ninja_id=ninja.id).count()
        misiones_completadas = AsignacionMision.query.filter_by(ninja_id=ninja.id, completada=True).count()
        
        reporte.append({
            'ninja': ninja.to_dict(),
            'misiones_asignadas': misiones_asignadas,
            'misiones_completadas': misiones_completadas
        })
    
    return jsonify(reporte)

@app.route('/api/reportes/misiones', methods=['GET'])
def reporte_misiones():
    misiones = Mision.query.all()
    reporte = []
    
    for mision in misiones:
        asignaciones = AsignacionMision.query.filter_by(mision_id=mision.id).all()
        ninjas_asignados = [asig.ninja.nombre for asig in asignaciones]
        completada = any(asig.completada for asig in asignaciones)
        
        reporte.append({
            'mision': mision.to_dict(),
            'ninjas_asignados': ninjas_asignados,
            'completada': completada
        })
    
    return jsonify(reporte)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)