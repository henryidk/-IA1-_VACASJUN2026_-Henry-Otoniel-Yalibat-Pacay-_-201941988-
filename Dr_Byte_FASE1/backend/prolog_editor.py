import re
import threading
import config

_lock_editor = threading.Lock()

# Patrones que identifican ÚNICAMENTE líneas de hechos (no cuerpos de reglas).
# Los hechos usan átomos en minúsculas y terminan en ').'
# Las llamadas dentro de reglas usan variables en mayúsculas o terminan en ','
_PAT_SINTOMA   = r'^sintoma\([a-z][a-z0-9_]*\)\.'
_PAT_DESC_S    = r'^descripcion_sintoma\('
_PAT_FALLA     = r'^falla\([a-z][a-z0-9_]*\)\.'
_PAT_DESC_F    = r'^descripcion_falla\('
_PAT_SF        = r'^sintoma_falla\('
_PAT_RECOM     = r'^recomendacion\('


def _leer():
    with open(config.PROLOG_FILE, 'r', encoding='utf-8') as f:
        return f.readlines()


def _escribir(lineas):
    with open(config.PROLOG_FILE, 'w', encoding='utf-8') as f:
        f.writelines(lineas)


def _ultima_linea(lineas, patron):
    """Índice de la última línea cuyo contenido (sin espacios) coincide con el patrón."""
    idx = -1
    for i, linea in enumerate(lineas):
        if re.search(patron, linea.strip()):
            idx = i
    return idx


def _recargar():
    from motor_prolog import recargar_prolog
    recargar_prolog()


# ------------------------------------------------------------------ SÍNTOMAS

def agregar_sintoma(id_sintoma, descripcion):
    with _lock_editor:
        lineas = _leer()

        idx = _ultima_linea(lineas, _PAT_SINTOMA)
        if idx == -1:
            return False, 'No se encontró la sección de síntomas'
        lineas.insert(idx + 1, f'sintoma({id_sintoma}).\n')

        idx_desc = _ultima_linea(lineas, _PAT_DESC_S)
        if idx_desc == -1:
            return False, 'No se encontró la sección de descripciones de síntomas'
        lineas.insert(idx_desc + 1, f"descripcion_sintoma({id_sintoma}, '{descripcion}').\n")

        _escribir(lineas)
        _recargar()
        return True, 'Síntoma agregado'


def eliminar_sintoma(id_sintoma):
    """Elimina el síntoma, su descripción y todas sus reglas sintoma_falla."""
    with _lock_editor:
        lineas = _leer()
        eid = re.escape(id_sintoma)
        patrones = [
            rf'^sintoma\({eid}\)\.',
            rf'^descripcion_sintoma\({eid},',
            rf'^sintoma_falla\({eid},',
        ]
        nuevas = [l for l in lineas if not any(re.search(p, l.strip()) for p in patrones)]
        _escribir(nuevas)
        _recargar()
        return True, 'Síntoma eliminado'


# -------------------------------------------------------------------- FALLAS

def agregar_falla(id_falla, descripcion):
    with _lock_editor:
        lineas = _leer()

        idx = _ultima_linea(lineas, _PAT_FALLA)
        if idx == -1:
            return False, 'No se encontró la sección de fallas'
        lineas.insert(idx + 1, f'falla({id_falla}).\n')

        idx_desc = _ultima_linea(lineas, _PAT_DESC_F)
        if idx_desc == -1:
            return False, 'No se encontró la sección de descripciones de fallas'
        lineas.insert(idx_desc + 1, f"descripcion_falla({id_falla}, '{descripcion}').\n")

        _escribir(lineas)
        _recargar()
        return True, 'Falla agregada'


def eliminar_falla(id_falla):
    """Elimina la falla, su descripción, sus reglas sintoma_falla y sus recomendaciones."""
    with _lock_editor:
        lineas = _leer()
        eid = re.escape(id_falla)
        patrones = [
            rf'^falla\({eid}\)\.',
            rf'^descripcion_falla\({eid},',
            rf'^sintoma_falla\([^,]+,\s*{eid}\)\.',
            rf'^recomendacion\({eid},',
        ]
        nuevas = [l for l in lineas if not any(re.search(p, l.strip()) for p in patrones)]
        _escribir(nuevas)
        _recargar()
        return True, 'Falla eliminada'


# -------------------------------------------------------------------- REGLAS

def agregar_regla(id_sintoma, id_falla):
    with _lock_editor:
        lineas = _leer()
        es, ef = re.escape(id_sintoma), re.escape(id_falla)

        if any(re.search(rf'^sintoma_falla\({es},\s*{ef}\)\.', l.strip()) for l in lineas):
            return False, 'La regla ya existe'

        idx = _ultima_linea(lineas, _PAT_SF)
        if idx == -1:
            return False, 'No se encontró la sección de reglas'
        lineas.insert(idx + 1, f'sintoma_falla({id_sintoma}, {id_falla}).\n')
        _escribir(lineas)
        _recargar()
        return True, 'Regla agregada'


def eliminar_regla(id_sintoma, id_falla):
    with _lock_editor:
        lineas = _leer()
        es, ef = re.escape(id_sintoma), re.escape(id_falla)
        patron = rf'^sintoma_falla\({es},\s*{ef}\)\.'
        nuevas = [l for l in lineas if not re.search(patron, l.strip())]
        _escribir(nuevas)
        _recargar()
        return True, 'Regla eliminada'


# --------------------------------------------------------- RECOMENDACIONES

def agregar_recomendacion(id_falla, texto):
    with _lock_editor:
        lineas = _leer()

        # Insertar junto a las recomendaciones de esa misma falla si ya existen
        idx = _ultima_linea(lineas, rf'^recomendacion\({re.escape(id_falla)},')
        if idx == -1:
            idx = _ultima_linea(lineas, _PAT_RECOM)
        if idx == -1:
            return False, 'No se encontró la sección de recomendaciones'

        texto_seguro = texto.replace("'", "\\'")
        lineas.insert(idx + 1, f"recomendacion({id_falla}, '{texto_seguro}').\n")
        _escribir(lineas)
        _recargar()
        return True, 'Recomendación agregada'


def eliminar_recomendacion(id_falla, texto):
    with _lock_editor:
        lineas = _leer()
        prefijo = f'recomendacion({id_falla},'
        nuevas = [l for l in lineas
                  if not (l.strip().startswith(prefijo) and texto in l)]
        _escribir(nuevas)
        _recargar()
        return True, 'Recomendación eliminada'


# --------------------------------------------------------------- EDICIÓN

def editar_descripcion_sintoma(id_sintoma, nueva_desc):
    with _lock_editor:
        lineas = _leer()
        eid = re.escape(id_sintoma)
        patron = rf'^descripcion_sintoma\({eid},'
        nueva_linea = f"descripcion_sintoma({id_sintoma}, '{nueva_desc}').\n"
        nuevas, encontrado = [], False
        for l in lineas:
            if re.search(patron, l.strip()):
                nuevas.append(nueva_linea)
                encontrado = True
            else:
                nuevas.append(l)
        if not encontrado:
            return False, 'Síntoma no encontrado'
        _escribir(nuevas)
        _recargar()
        return True, 'Síntoma actualizado'


def editar_descripcion_falla(id_falla, nueva_desc):
    with _lock_editor:
        lineas = _leer()
        eid = re.escape(id_falla)
        patron = rf'^descripcion_falla\({eid},'
        nueva_linea = f"descripcion_falla({id_falla}, '{nueva_desc}').\n"
        nuevas, encontrado = [], False
        for l in lineas:
            if re.search(patron, l.strip()):
                nuevas.append(nueva_linea)
                encontrado = True
            else:
                nuevas.append(l)
        if not encontrado:
            return False, 'Falla no encontrada'
        _escribir(nuevas)
        _recargar()
        return True, 'Falla actualizada'


def editar_recomendacion(id_falla, texto_viejo, texto_nuevo):
    with _lock_editor:
        lineas = _leer()
        prefijo = f'recomendacion({id_falla},'
        texto_nuevo_seguro = texto_nuevo.replace("'", "\\'")
        nueva_linea = f"recomendacion({id_falla}, '{texto_nuevo_seguro}').\n"
        nuevas, encontrado = [], False
        for l in lineas:
            if l.strip().startswith(prefijo) and texto_viejo in l:
                nuevas.append(nueva_linea)
                encontrado = True
            else:
                nuevas.append(l)
        if not encontrado:
            return False, 'Recomendación no encontrada'
        _escribir(nuevas)
        _recargar()
        return True, 'Recomendación actualizada'


def editar_regla(id_sintoma, falla_vieja, falla_nueva):
    with _lock_editor:
        lineas = _leer()
        es = re.escape(id_sintoma)
        ef_nueva = re.escape(falla_nueva)

        if any(re.search(rf'^sintoma_falla\({es},\s*{ef_nueva}\)\.', l.strip()) for l in lineas):
            return False, 'La regla ya existe'

        patron_viejo = rf'^sintoma_falla\({es},\s*{re.escape(falla_vieja)}\)\.'
        nueva_linea = f'sintoma_falla({id_sintoma}, {falla_nueva}).\n'
        nuevas, encontrado = [], False
        for l in lineas:
            if re.search(patron_viejo, l.strip()):
                nuevas.append(nueva_linea)
                encontrado = True
            else:
                nuevas.append(l)
        if not encontrado:
            return False, 'Regla no encontrada'
        _escribir(nuevas)
        _recargar()
        return True, 'Regla actualizada'
