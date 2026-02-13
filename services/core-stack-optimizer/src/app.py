# from flask import Flask

# from src.util.config_loader import Config
# from src.data.stack_optimizer_loaded_data import StackOptimizerLoadedData
# from src.util.flask_helper import pre_post_process

# app = Flask(__name__)

# @app.before_first_request
# def read_files():
#     StackOptimizerLoadedData.read_files_if_required()


# @app.route('/optimize', methods=['POST'])
# @pre_post_process
# def batch(data):
#     responses = []
#     for req in data:
#         response = "optimization function call"
#         responses.append(response)
#     return responses

# @app.route('/message', methods=['GET'])
# def hello_world():
#     return 'hello'

# if __name__ == '__main__':
#     appPort = Config.value('port')
#     app.run(host='0.0.0.0', port=appPort)

