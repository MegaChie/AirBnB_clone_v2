from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route('/', strict_slashes=False)
    def home():
        return "Hello HBNB!"

    return app
