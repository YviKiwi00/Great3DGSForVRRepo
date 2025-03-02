import os
import sys
from flask import Flask

sys.path.append(os.path.dirname(__file__))

from controllers.upload_controller import upload_blueprint
from controllers.jobs_controller import jobs_blueprint

app = Flask(__name__)

# Register all controllers
app.register_blueprint(upload_blueprint)
app.register_blueprint(jobs_blueprint)

if __name__ == "__main__":
    app.run(port=8000)