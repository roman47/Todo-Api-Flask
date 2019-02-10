# test_todos.py
import unittest
import os
import json
from app import create_app
from models import DATABASE,Todo
from flask import request




class TodoTestCase(unittest.TestCase):
    """This class represents the todo test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.todo = {'name': 'Get a new haircut'}
        #import pdb;
        #pdb.set_trace()

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            DATABASE.connect(reuse_if_open=True)
            DATABASE.create_tables([Todo], safe=True)
            DATABASE.close()

    def test_todo_creation(self):
        """Test API can create a todo (POST request)"""
        #import pdb;
        #pdb.set_trace()
        res = self.client().post('/api/v1/todos', data=self.todo)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Get a new haircut', str(res.data))

    def test_api_can_get_all_todos(self):
        """Test API can get a todo (GET request)."""
        res = self.client().post('/api/v1/todos', data=self.todo)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/todos')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Get a new haircut', str(res.data))

    def test_api_can_get_todo_by_id(self):
        """Test API can get a single todo by using it's id."""
        rv = self.client().post('/api/v1/todos', data=self.todo)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/api/v1/todos/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Get a new haircut', str(result.data))

    def test_todo_can_be_edited(self):
        """Test API can edit an existing todo. (PUT request)"""
        rv = self.client().post(
            '/api/v1/todos',
            data={'name': 'Have fun'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/api/v1/todos/1',
            data={
                "name": "have a _LOT_ of fun"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/api/v1/todos/1')
        self.assertIn('Dont just eat', str(results.data))

    def test_todo_deletion(self):
        """Test API can delete an existing todo. (DELETE request)."""
        rv = self.client().post(
            '/api/v1/todos',
            data={'name': 'Eat, pray and love'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/api/v1/todos/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/api/v1/todos/1')
        self.assertEqual(result.status_code, 404)


    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            DATABASE.close()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
