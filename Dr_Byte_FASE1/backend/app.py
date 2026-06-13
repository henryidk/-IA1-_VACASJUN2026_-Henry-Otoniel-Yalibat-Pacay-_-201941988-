from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    from routes.diagnostico import diagnostico_bp
    from routes.historial import historial_bp
    from routes.admin import admin_bp
    app.register_blueprint(diagnostico_bp, url_prefix='/api')
    app.register_blueprint(historial_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api')

    @app.errorhandler(404)
    def not_found(e):
        return {'error': 'Ruta no encontrada'}, 404

    @app.errorhandler(500)
    def server_error(e):
        return {'error': 'Error interno del servidor'}, 500

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
