# app.py - Microservicio de gestión de tareas (Flask API)
import os
import logging
from datetime import datetime, timezone
from flask import Flask, jsonify, request

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Almacenamiento en memoria (se puede migrar a Redis/DB)
tareas = []
contador_id = 0


def obtener_siguiente_id():
    """Genera un ID autoincremental para las tareas."""
    global contador_id
    contador_id += 1
    return contador_id


# ─────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint para monitoreo y orquestación."""
    logger.info("Health check solicitado")
    return jsonify({
        "status": "healthy",
        "service": "microservicio-tareas",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": os.getenv("APP_VERSION", "1.0.0")
    }), 200


@app.route('/tareas', methods=['GET'])
def listar_tareas():
    """Lista todas las tareas registradas."""
    logger.info(f"Listando tareas — total: {len(tareas)}")
    return jsonify({"tareas": tareas, "total": len(tareas)}), 200


@app.route('/tareas', methods=['POST'])
def agregar_tarea():
    """Crea una nueva tarea. Requiere campo 'titulo' en el body JSON."""
    datos = request.get_json()

    if not datos or 'titulo' not in datos:
        logger.warning("Solicitud rechazada: falta campo 'titulo'")
        return jsonify({"error": "El campo 'titulo' es requerido"}), 400

    titulo = datos['titulo'].strip()
    if not titulo:
        logger.warning("Solicitud rechazada: título vacío")
        return jsonify({"error": "El título no puede estar vacío"}), 400

    tarea = {
        "id": obtener_siguiente_id(),
        "titulo": titulo,
        "completada": False,
        "creada_en": datetime.now(timezone.utc).isoformat()
    }
    tareas.append(tarea)
    logger.info(f"Tarea creada: id={tarea['id']}, titulo='{tarea['titulo']}'")
    return jsonify(tarea), 201


@app.route('/tareas/<int:tarea_id>', methods=['GET'])
def obtener_tarea(tarea_id):
    """Obtiene una tarea por su ID."""
    tarea = next((t for t in tareas if t["id"] == tarea_id), None)
    if not tarea:
        logger.warning(f"Tarea no encontrada: id={tarea_id}")
        return jsonify({"error": "Tarea no encontrada"}), 404
    return jsonify(tarea), 200


@app.route('/tareas/<int:tarea_id>', methods=['PUT'])
def completar_tarea(tarea_id):
    """Marca una tarea como completada."""
    tarea = next((t for t in tareas if t["id"] == tarea_id), None)
    if not tarea:
        logger.warning(f"Tarea no encontrada para completar: id={tarea_id}")
        return jsonify({"error": "Tarea no encontrada"}), 404

    tarea["completada"] = True
    tarea["completada_en"] = datetime.now(timezone.utc).isoformat()
    logger.info(f"Tarea completada: id={tarea_id}")
    return jsonify(tarea), 200


@app.route('/tareas/<int:tarea_id>', methods=['DELETE'])
def eliminar_tarea(tarea_id):
    """Elimina una tarea por su ID."""
    global tareas
    tarea = next((t for t in tareas if t["id"] == tarea_id), None)
    if not tarea:
        logger.warning(f"Tarea no encontrada para eliminar: id={tarea_id}")
        return jsonify({"error": "Tarea no encontrada"}), 404

    tareas = [t for t in tareas if t["id"] != tarea_id]
    logger.info(f"Tarea eliminada: id={tarea_id}")
    return jsonify({"mensaje": "Tarea eliminada correctamente"}), 200


# ─────────────────────────────────────────────
# Punto de entrada
# ─────────────────────────────────────────────

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    logger.info(f"Iniciando microservicio de tareas en puerto {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)