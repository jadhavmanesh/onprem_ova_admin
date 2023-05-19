#!/opt/miniconda3/bin/python3
__author__ = "Vishnu Prasad"
__version__ = "1.0"
__status__ = "Production"

import argparse
import gc

from flask import Flask
from flask_compress import Compress
from flask_cors import CORS

from scripts.constants.app_configuration import app_config
from scripts.constants.app_constants import FlaskService
from scripts.services.service import serv

gc.collect()
app = Flask(__name__)
app.config["COMPRESS_LEVEL"] = 6
Compress(app=app)
app.register_blueprint(serv)
CORS(app, orgins="*",
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
     supports_credentials=True, intercept_exceptions=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app_config[FlaskService.config_section][FlaskService.port], debug=True, threaded=True,
            use_reloader=True)
