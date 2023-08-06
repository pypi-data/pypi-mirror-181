import os
import flask
import logging
from module_placeholder.ui import jinja
from module_placeholder.authentication import safe_api_call
from module_placeholder.config import read_config

logger = logging.getLogger(__name__)

config = read_config("config.yml")
api_key = config['api_key']
# Adjust base name depending on environment
app_name = "" if os.environ.get('SERVER_RUNNING_LOCALLY', "FALSE") == "TRUE" else "automation_template"


def register_routes(app):

    @app.route('/', methods=['get'])
    @safe_api_call
    def get_index():
        template = jinja.get_template('index.html')
        return flask.Response(template.render(api_key=api_key, app_name=app_name))
