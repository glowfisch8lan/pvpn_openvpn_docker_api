from flask import Blueprint

from src.middlewares.AuthMiddleware import AuthMiddleware
from src.modules.vpn.ConfigController import ConfigController as VPNConfigController
from src.modules.vpn.MainController import MainController as VPNMainController
from src.modules.vpn.UserController import UserController as VPNUserController
# from src.modules.vpn.LogController import LogController as VPNLogController

def api():
    apiBlueprint = Blueprint('api', __name__)

    # apiBlueprint.add_url_rule(rule='/vpn/connected', view_func=VPNUserController().connected, methods=['GET'])
    apiBlueprint.add_url_rule(rule='/vpn/create_config', view_func=VPNConfigController().create, methods=['POST'])
    # apiBlueprint.add_url_rule(rule='/vpn/routing', view_func=VPNUserController().routing, methods=['GET'])
    # apiBlueprint.add_url_rule(rule='/vpn/log', view_func=VPNLogController().log, methods=['GET'])
    # apiBlueprint.add_url_rule(rule='/user/keys', view_func=VPNUserController().keys, methods=['GET'])
    # apiBlueprint.add_url_rule(rule='/vpn/config/info', view_func=VPNConfigController().info, methods=['POST'])
    apiBlueprint.add_url_rule(rule='/vpn/disable', view_func=VPNUserController().disable, methods=['POST'])
    apiBlueprint.add_url_rule(rule='/vpn/enable', view_func=VPNUserController().enable, methods=['POST'])

    return apiBlueprint

def route(app) -> None:
    app.add_url_rule(rule='/', view_func=VPNMainController().index, methods=['GET'])
    app.add_url_rule(rule='/vpn/<cn>', view_func=VPNConfigController().download_file, methods=['GET'])
    app.register_blueprint(api(), url_prefix='/api')


    app.before_request_funcs = {
        'api': [AuthMiddleware().handle]
    }

    return None
