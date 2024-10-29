from flask import Flask, current_app

from calculator.api.rpn import rpn_bp
from calculator.db import db
from config import Config




def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(rpn_bp)

    db.init_app(app)

    @app.route('/swagger.yaml')
    def swagger_spec():
        return current_app.send_static_file('swagger.yaml')

    @app.route('/')
    def swagger_ui():
        return current_app.send_static_file('swagger.html')

    return app



if __name__=="__main__":
    app = create_app()
    app.run()