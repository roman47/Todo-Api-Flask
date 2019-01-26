from flask import jsonify, Blueprint, abort

from flask_restful import (Resource, Api, reqparse,
                               inputs, fields, marshal,
                               marshal_with, url_for)

import models

todo_fields = {
    'name': fields.String,
}


def todo_or_404(todo_id):
    """if a todo doesn't exist, return a good error message"""
    try:
        todo = models.Todo.get(models.Todo.id == todo_id)
    except models.Todo.DoesNotExist:
        abort(404)
    else:
        return todo


class TodoList(Resource):
    """This class represents the set of todos"""
    def __init__(self):
        """Start up the TodoList resource class"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No todo name provided',
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        """Get the set of todos"""
        todos = [marshal(todo, todo_fields)
                   for todo in models.Todo.select()]
        return todos

    @marshal_with(todo_fields)
    def post(self):
        """Create a new todo"""
        args = self.reqparse.parse_args()
        todo = models.Todo.create(**args)
        #import pdb;
        #pdb.set_trace()
        return (todo, 201, {
            'Location': url_for('resources.todos.todo', id=todo.id)}
                )


class Todo(Resource):
    """This class represents a single todo"""
    def __init__(self):
        """Start up the Todo resource class"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No todo name provided',
            location=['form', 'json']
        )
        super().__init__()

    @marshal_with(todo_fields)
    def get(self, id):
        """Get a todo"""
        return todo_or_404(id)

    @marshal_with(todo_fields)
    def put(self, id):
        """Put a change into a todo"""
        args = self.reqparse.parse_args()
        query = models.Todo.update(**args).where(models.Todo.id == id)
        query.execute()
        return (models.Todo.get(models.Todo.id == id), 200,
                {'Location': url_for('resources.todos.todo', id=id)})

    def delete(self, id):
        """Delete a todo"""
        query = models.Todo.delete().where(models.Todo.id == id)
        query.execute()
        return '', 204, {'Location': url_for('resources.todos.todos')}


todos_api = Blueprint('resources.todos', __name__)
api = Api(todos_api)
api.add_resource(
    TodoList,
    '/api/v1/todos',
    endpoint='todos'
)
api.add_resource(
    Todo,
    '/api/v1/todos/<int:id>',
    endpoint='todo'
)