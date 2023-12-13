from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager
from os import path

mysql = MySQL()
DB_NAME = "notes"
DB_USER = "root"
DB_PASSWORD = "July82001Cl@ro"
DB_HOST = "localhost"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['MYSQL_USER'] = DB_USER
    app.config['MYSQL_PASSWORD'] = DB_PASSWORD
    app.config['MYSQL_DB'] = DB_NAME
    app.config['MYSQL_HOST'] = DB_HOST
    mysql.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    with app.app_context():
        # Load and execute schema.sql
        with app.open_resource('schema.sql', mode='r') as f:
            cursor = mysql.connection.cursor()
            cursor.execute(f.read(), multi=True)
            mysql.connection.commit()
            cursor.close()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    print(f"Database connection established: {app.config['MYSQL_DB']}")

    return app
