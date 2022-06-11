from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from routes import frontend_blueprint

app = Flask(__name__, static_folder="static")

app.config['SECRET_KEY'] = "7-kDpFSq5bIzMcpW8ZXH-w"
app.config['WTF_CSRF_SECRET_KEY'] = "SIc_zrD_W2C8LfM_DByN6w"
app.config['UPLOAD_FOLDER'] = "static/images"

app.register_blueprint(frontend_blueprint)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_message = "Please login"
login_manager.login_view = "frontend.login"

bootstrap = Bootstrap(app)


@login_manager.user_loader
def load_user(user_id):
    return None


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


