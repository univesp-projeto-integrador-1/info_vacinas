# project/server/__init__.py
import os

from flask import Flask, render_template
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# instantiate the extensions
login_manager = LoginManager()
bcrypt = Bcrypt()
toolbar = DebugToolbarExtension()
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
admin = Admin(template_mode='bootstrap4')


def create_app(script_info=None):
    from project.server.models import (CategoriaIdade, PeriodoIdade, User,
                                       Vacina)

    # instantiate the app
    app = Flask(
        __name__,
        template_folder="../client/templates",
        static_folder="../client/static",
    )

    # set config
    app_settings = os.getenv(
        "APP_SETTINGS", "project.server.config.ProductionConfig"
    )
    app.config.from_object(app_settings)

    # set up extensions
    login_manager.init_app(app)
    bcrypt.init_app(app)
    toolbar.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    admin = Admin(template_mode='bootstrap4')
    admin.init_app(app, index_view=AdminIndexView(),
                   endpoint='admin', url='/admin')

    # register blueprints
    from project.server.main.views import main_blueprint
    from project.server.user.views import user_blueprint

    app.register_blueprint(user_blueprint)
    app.register_blueprint(main_blueprint)

    # flask-admin
    admin.add_view(ModelView(User, db.session,
                             endpoint='usuario_admin', name="Usuários"))
    admin.add_view(ModelView(Vacina, db.session,
                             endpoint='/vacina', name="Vacina"))
    admin.add_view(ModelView(CategoriaIdade, db.session,
                             endpoint='categoria_idade', name="Categoria idade"))
    admin.add_view(ModelView(PeriodoIdade, db.session,
                             endpoint='periodo_idade', name="Período idade"))

    login_manager.login_view = "user.login"
    login_manager.login_message_category = "danger"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()

    # error handlers
    @app.errorhandler(401)
    def unauthorized_page(error):
        return render_template("errors/401.html"), 401

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("errors/500.html"), 500

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
