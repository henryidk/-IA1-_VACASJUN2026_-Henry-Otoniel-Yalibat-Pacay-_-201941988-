import re
from flask import Blueprint, request, jsonify
import motor_prolog as motor
import prolog_editor as editor
import bot_config

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


@admin_bp.put('/admin/sintomas/<string:id_sintoma>')
def editar_sintoma(id_sintoma):
    datos = request.get_json() or {}
    desc = datos.get('descripcion', '').strip()
    if not desc:
        return jsonify({'error': 'La descripción es obligatoria'}), 400
    ok, msg = editor.editar_descripcion_sintoma(id_sintoma, desc)
    return jsonify({'mensaje': msg}) if ok else (jsonify({'error': msg}), 404)


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


@admin_bp.put('/admin/fallas/<string:id_falla>')
def editar_falla(id_falla):
    datos = request.get_json() or {}
    desc = datos.get('descripcion', '').strip()
    if not desc:
        return jsonify({'error': 'La descripción es obligatoria'}), 400
    ok, msg = editor.editar_descripcion_falla(id_falla, desc)
    return jsonify({'mensaje': msg}) if ok else (jsonify({'error': msg}), 404)


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


@admin_bp.put('/admin/reglas/<string:sintoma>/<string:falla_vieja>')
def editar_regla(sintoma, falla_vieja):
    datos = request.get_json() or {}
    falla_nueva = datos.get('falla_nueva', '').strip()
    if _id_invalido(sintoma) or _id_invalido(falla_vieja) or _id_invalido(falla_nueva):
        return jsonify({'error': 'Ids inválidos'}), 400
    ok, msg = editor.editar_regla(sintoma, falla_vieja, falla_nueva)
    return jsonify({'mensaje': msg}) if ok else (jsonify({'error': msg}), 409)


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


@admin_bp.put('/admin/recomendaciones')
def editar_recomendacion():
    datos = request.get_json() or {}
    falla       = datos.get('falla', '').strip()
    texto_viejo = datos.get('texto_viejo', '').strip()
    texto_nuevo = datos.get('texto_nuevo', '').strip()

    if _id_invalido(falla) or not texto_viejo or not texto_nuevo:
        return jsonify({'error': 'falla, texto_viejo y texto_nuevo son obligatorios'}), 400

    ok, msg = editor.editar_recomendacion(falla, texto_viejo, texto_nuevo)
    return jsonify({'mensaje': msg}) if ok else (jsonify({'error': msg}), 404)


@admin_bp.delete('/admin/recomendaciones')
def eliminar_recomendacion():
    datos = request.get_json() or {}
    falla = datos.get('falla', '').strip()
    texto = datos.get('texto', '').strip()

    if _id_invalido(falla) or not texto:
        return jsonify({'error': 'falla y texto son obligatorios'}), 400

    ok, msg = editor.eliminar_recomendacion(falla, texto)
    return jsonify({'mensaje': msg}) if ok else (jsonify({'error': msg}), 500)


# ============================================================ CONFIG BOT

@admin_bp.get('/admin/config/bot')
def obtener_config_bot():
    cfg = bot_config.leer_config()
    token = cfg['token']
    return jsonify({
        'token':      ('*' * 8 + token[-4:]) if len(token) > 4 else '',
        'chat_id':    cfg['chat_id'],
        'activo':     cfg['activo'],
        'encabezado': cfg['encabezado'],
    })


@admin_bp.put('/admin/config/bot')
def actualizar_config_bot():
    datos = request.get_json() or {}

    token      = datos.get('token', '').strip()
    chat_id    = datos.get('chat_id', '').strip()
    activo     = datos.get('activo')
    encabezado = datos.get('encabezado', '').strip()

    if activo is None or not isinstance(activo, bool):
        return jsonify({'error': 'El campo activo debe ser true o false'}), 400
    if not encabezado:
        return jsonify({'error': 'El encabezado no puede estar vacío'}), 400

    bot_config.guardar_config({
        'token':      token,
        'chat_id':    chat_id,
        'activo':     activo,
        'encabezado': encabezado,
    })
    return jsonify({'mensaje': 'Configuración del bot actualizada correctamente'})
