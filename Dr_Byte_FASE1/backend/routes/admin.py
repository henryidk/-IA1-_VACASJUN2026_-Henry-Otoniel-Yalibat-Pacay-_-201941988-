import re
from flask import Blueprint, request, jsonify
import motor_prolog as motor
import prolog_editor as editor

admin_bp = Blueprint('admin', __name__)

_ID_VALIDO = re.compile(r'^[a-z][a-z0-9_]*$')


def _id_invalido(valor):
    return not _ID_VALIDO.match(valor or '')


# ================================================================ SÍNTOMAS

@admin_bp.get('/admin/sintomas')
def listar_sintomas():
    return jsonify(motor.obtener_sintomas())


@admin_bp.post('/admin/sintomas')
def crear_sintoma():
    datos = request.get_json() or {}
    id_s = datos.get('id', '').strip()
    desc = datos.get('descripcion', '').strip()

    if _id_invalido(id_s):
        return jsonify({'error': 'El id debe ser una cadena en minúsculas sin espacios'}), 400
    if not desc:
        return jsonify({'error': 'La descripción es obligatoria'}), 400

    ok, msg = editor.agregar_sintoma(id_s, desc)
    return (jsonify({'mensaje': msg}), 201) if ok else (jsonify({'error': msg}), 409)


@admin_bp.delete('/admin/sintomas/<string:id_sintoma>')
def eliminar_sintoma(id_sintoma):
    if _id_invalido(id_sintoma):
        return jsonify({'error': 'Id inválido'}), 400
    ok, msg = editor.eliminar_sintoma(id_sintoma)
    return jsonify({'mensaje': msg}) if ok else (jsonify({'error': msg}), 500)


# ================================================================== FALLAS

@admin_bp.get('/admin/fallas')
def listar_fallas():
    return jsonify(motor.obtener_fallas())


@admin_bp.post('/admin/fallas')
def crear_falla():
    datos = request.get_json() or {}
    id_f = datos.get('id', '').strip()
    desc = datos.get('descripcion', '').strip()

    if _id_invalido(id_f):
        return jsonify({'error': 'El id debe ser una cadena en minúsculas sin espacios'}), 400
    if not desc:
        return jsonify({'error': 'La descripción es obligatoria'}), 400

    ok, msg = editor.agregar_falla(id_f, desc)
    return (jsonify({'mensaje': msg}), 201) if ok else (jsonify({'error': msg}), 409)


@admin_bp.delete('/admin/fallas/<string:id_falla>')
def eliminar_falla(id_falla):
    if _id_invalido(id_falla):
        return jsonify({'error': 'Id inválido'}), 400
    ok, msg = editor.eliminar_falla(id_falla)
    return jsonify({'mensaje': msg}) if ok else (jsonify({'error': msg}), 500)


# ================================================================== REGLAS

@admin_bp.get('/admin/reglas')
def listar_reglas():
    return jsonify(motor.obtener_reglas())


@admin_bp.post('/admin/reglas')
def crear_regla():
    datos = request.get_json() or {}
    sintoma = datos.get('sintoma', '').strip()
    falla   = datos.get('falla', '').strip()

    if _id_invalido(sintoma) or _id_invalido(falla):
        return jsonify({'error': 'sintoma y falla deben ser ids válidos'}), 400

    ok, msg = editor.agregar_regla(sintoma, falla)
    return (jsonify({'mensaje': msg}), 201) if ok else (jsonify({'error': msg}), 409)


@admin_bp.delete('/admin/reglas/<string:sintoma>/<string:falla>')
def eliminar_regla(sintoma, falla):
    if _id_invalido(sintoma) or _id_invalido(falla):
        return jsonify({'error': 'Ids inválidos'}), 400
    ok, msg = editor.eliminar_regla(sintoma, falla)
    return jsonify({'mensaje': msg}) if ok else (jsonify({'error': msg}), 500)


# ============================================================ RECOMENDACIONES

@admin_bp.get('/admin/recomendaciones')
def listar_recomendaciones():
    return jsonify(motor.obtener_recomendaciones())


@admin_bp.get('/admin/recomendaciones/<string:id_falla>')
def listar_recomendaciones_falla(id_falla):
    if _id_invalido(id_falla):
        return jsonify({'error': 'Id inválido'}), 400
    return jsonify(motor.obtener_recomendaciones(id_falla))


@admin_bp.post('/admin/recomendaciones')
def crear_recomendacion():
    datos = request.get_json() or {}
    falla = datos.get('falla', '').strip()
    texto = datos.get('texto', '').strip()

    if _id_invalido(falla):
        return jsonify({'error': 'El id de falla es inválido'}), 400
    if not texto:
        return jsonify({'error': 'El texto es obligatorio'}), 400

    ok, msg = editor.agregar_recomendacion(falla, texto)
    return (jsonify({'mensaje': msg}), 201) if ok else (jsonify({'error': msg}), 500)


@admin_bp.delete('/admin/recomendaciones')
def eliminar_recomendacion():
    datos = request.get_json() or {}
    falla = datos.get('falla', '').strip()
    texto = datos.get('texto', '').strip()

    if _id_invalido(falla) or not texto:
        return jsonify({'error': 'falla y texto son obligatorios'}), 400

    ok, msg = editor.eliminar_recomendacion(falla, texto)
    return jsonify({'mensaje': msg}) if ok else (jsonify({'error': msg}), 500)
