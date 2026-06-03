"""Flask application factory."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

from app.config import Config

# Extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()
csrf = CSRFProtect()


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    csrf.init_app(app)

    # Login manager settings
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    # User loader
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Create tables & seed admin on first run
    with app.app_context():
        from app.models import Settings
        db.create_all()
        _seed_defaults(app)

    return app


def _seed_defaults(app):
    """Seed the database with default admin and settings."""
    from app.models import User, Settings
    from werkzeug.security import generate_password_hash

    # Create default admin if not exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@library.com',
            password_hash=generate_password_hash('admin123'),
            full_name='System Administrator',
            role='admin',
            is_approved=True,
            is_active=True,
        )
        db.session.add(admin)

    # Create default settings if not exists
    settings = Settings.query.first()
    if not settings:
        settings = Settings(
            late_fee_per_day=app.config.get('LATE_FEE_PER_DAY', 5.00)
        )
        db.session.add(settings)

    db.session.commit()
