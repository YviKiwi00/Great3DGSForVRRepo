from flask import Flask
from controllers.upload_controller import upload_blueprint

app = Flask(__name__)

# Register all controllers
app.register_blueprint(upload_blueprint)

if __name__ == "__main__":
    app.run(port=8000)