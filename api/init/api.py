import logging
import sys
import os
from flask import Blueprint, Flask, url_for
from flask_cors import CORS
from flask_login import LoginManager
from flask_restplus import Api
from health.routes import register_health
from proxy.routes import register_graphql
from security.routes import register_security

log = logging.getLogger(__name__)
logging.basicConfig(
    # filename='mobydq.log',
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create flask app and enable cross origin resource sharing
app = Flask(__name__)
CORS(app)
login = LoginManager(app)

# Get a cryptographically secure random sequence of bytes to be used as the app's secret_key
app.secret_key = os.urandom(24)

# This is required to fix swagger UI not loading issue due to https
@property
def swagger_url(self):
    """Patch for HTTPS"""
    return url_for(self.endpoint('specs'), _external=True, _scheme='https')

# Create blueprint to indicate api base url
blueprint = Blueprint('api', __name__, url_prefix='/mobydq/api')


# Create Swagger documentation for blueprint
api = Api(
    blueprint,
    title='MobyDQ API',
    version='v1',
    description='API used to configure and trigger the execution of data quality indicators.',
    doc='/doc',
    contact=os.environ['MAIL_SENDER'])

# This is required to fix swagger UI not loading issue due to https
Api.specs_url = swagger_url
app.register_blueprint(blueprint)

# Declare resources name spaces
api.namespaces.clear()
graphql = api.namespace('GraphQL', path='/v1')
health = api.namespace('Health', path='/v1')
security = api.namespace('Security', path='/v1')

# Register all API resources
register_health(health)
register_graphql(graphql, api)
register_security(security)
