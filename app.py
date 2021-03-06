from flask import Flask, g, jsonify, render_template

import config
import models
from resources.todos import todos_api
from models import DATABASE,Todo
app = Flask(__name__)
app.register_blueprint(todos_api)


@app.route('/')
def my_todos():
    """The main entry point of the app"""
    return render_template('index.html')


def create_app():
    #app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
    DATABASE.connect(reuse_if_open=True)
    DATABASE.create_tables([Todo], safe=True)
    DATABASE.close()
    return app


if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
