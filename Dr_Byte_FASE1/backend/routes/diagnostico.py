from flask import Blueprint, request, jsonify
from motor_prolog import obtener_diagnostico, obtener_sintomas
from historial import guardar_diagnostico

diagnostico_bp = Blueprint('diagnostico', __name__)


@diagnostico_bp.route('/sintomas', methods=['GET'])
def listar_sintomas():
    sintomas = obtener_sintomas()
    return jsonify({'sintomas': sintomas}), 200


@diagnostico_bp.route('/diagnose', methods=['POST'])
def diagnosticar():
    data = request.get_json()

    if not data or 'sintomas' not in data:
        return jsonify({'error': 'Se requiere una lista de síntomas'}), 400

    sintomas = data['sintomas']

    if not isinstance(sintomas, list) or len(sintomas) == 0:
        return jsonify({'error': 'Los síntomas deben ser una lista no vacía'}), 400

    resultado = obtener_diagnostico(sintomas)

    if not resultado:
        return jsonify({'error': 'No se encontró diagnóstico para los síntomas indicados'}), 404

    entrada = guardar_diagnostico(
        sintomas,
        resultado['falla'],
        resultado['descripcion'],
        resultado['recomendaciones']
    )

    return jsonify({**resultado, 'id': entrada['id'], 'fecha': entrada['fecha']}), 200
