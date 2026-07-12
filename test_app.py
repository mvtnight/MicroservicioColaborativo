# test_app.py - Tests unitarios del microservicio de tareas
# Usa pytest y el test client de Flask para probar todos los endpoints

import pytest
from app import app


@pytest.fixture
def client():
    """Crea un cliente de pruebas de Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Reiniciar estado entre tests
        from app import tareas
        tareas.clear()
        import app as app_module
        app_module.contador_id = 0
        yield client


class TestHealthCheck:
    """Tests para el endpoint de health check."""

    def test_health_check_retorna_200(self, client):
        """Verifica que el health check responde correctamente."""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert data['service'] == 'microservicio-tareas'
        assert 'timestamp' in data

    def test_health_check_incluye_version(self, client):
        """Verifica que el health check incluye la versión."""
        response = client.get('/health')
        data = response.get_json()
        assert 'version' in data


class TestAgregarTarea:
    """Tests para el endpoint POST /tareas."""

    def test_agregar_tarea_exitosamente(self, client):
        """Verifica que se puede agregar una tarea con título válido."""
        response = client.post('/tareas', json={"titulo": "Configurar Git"})
        assert response.status_code == 201
        data = response.get_json()
        assert data['titulo'] == "Configurar Git"
        assert data['completada'] is False
        assert data['id'] == 1

    def test_agregar_tarea_sin_titulo_retorna_400(self, client):
        """Verifica que se rechaza una tarea sin título."""
        response = client.post('/tareas', json={})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_agregar_tarea_titulo_vacio_retorna_400(self, client):
        """Verifica que se rechaza una tarea con título vacío."""
        response = client.post('/tareas', json={"titulo": "  "})
        assert response.status_code == 400

    def test_agregar_tarea_sin_json_retorna_error(self, client):
        """Verifica que se rechaza una petición sin body JSON."""
        response = client.post('/tareas')
        assert response.status_code in (400, 415)  # 415 si no hay Content-Type JSON


class TestListarTareas:
    """Tests para el endpoint GET /tareas."""

    def test_listar_tareas_vacia(self, client):
        """Verifica que la lista inicial está vacía."""
        response = client.get('/tareas')
        assert response.status_code == 200
        data = response.get_json()
        assert data['tareas'] == []
        assert data['total'] == 0

    def test_listar_tareas_con_datos(self, client):
        """Verifica que se listan las tareas después de agregar."""
        client.post('/tareas', json={"titulo": "Tarea 1"})
        client.post('/tareas', json={"titulo": "Tarea 2"})
        response = client.get('/tareas')
        data = response.get_json()
        assert data['total'] == 2
        assert len(data['tareas']) == 2


class TestObtenerTarea:
    """Tests para el endpoint GET /tareas/<id>."""

    def test_obtener_tarea_existente(self, client):
        """Verifica que se puede obtener una tarea por ID."""
        client.post('/tareas', json={"titulo": "Tarea de prueba"})
        response = client.get('/tareas/1')
        assert response.status_code == 200
        data = response.get_json()
        assert data['titulo'] == "Tarea de prueba"

    def test_obtener_tarea_inexistente_retorna_404(self, client):
        """Verifica que se retorna 404 para un ID inexistente."""
        response = client.get('/tareas/999')
        assert response.status_code == 404


class TestCompletarTarea:
    """Tests para el endpoint PUT /tareas/<id>."""

    def test_completar_tarea_exitosamente(self, client):
        """Verifica que se puede marcar una tarea como completada."""
        client.post('/tareas', json={"titulo": "Tarea para completar"})
        response = client.put('/tareas/1')
        assert response.status_code == 200
        data = response.get_json()
        assert data['completada'] is True
        assert 'completada_en' in data

    def test_completar_tarea_inexistente_retorna_404(self, client):
        """Verifica que se retorna 404 al completar tarea inexistente."""
        response = client.put('/tareas/999')
        assert response.status_code == 404


class TestEliminarTarea:
    """Tests para el endpoint DELETE /tareas/<id>."""

    def test_eliminar_tarea_exitosamente(self, client):
        """Verifica que se puede eliminar una tarea."""
        client.post('/tareas', json={"titulo": "Tarea a eliminar"})
        response = client.delete('/tareas/1')
        assert response.status_code == 200
        # Verificar que ya no existe
        response = client.get('/tareas/1')
        assert response.status_code == 404

    def test_eliminar_tarea_inexistente_retorna_404(self, client):
        """Verifica que se retorna 404 al eliminar tarea inexistente."""
        response = client.delete('/tareas/999')
        assert response.status_code == 404