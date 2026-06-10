from flask import Blueprint, jsonify
from historial import obtener_historial, obtener_por_id

historial_bp = Blueprint('historial', __name__)


@historial_bp.route('/history', methods=['GET'])
def listar_historial():
    registros = obtener_historial()
    return jsonify({'historial': registros, 'total': len(registros)}), 200


@historial_bp.route('/history/<int:id_diagnostico>', methods=['GET'])
def obtener_diagnostico(id_diagnostico):
    registro = obtener_por_id(id_diagnostico)

    if not registro:
        return jsonify({'error': f'No se encontró diagnóstico con id {id_diagnostico}'}), 404

    return jsonify(registro), 200
