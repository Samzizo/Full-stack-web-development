import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from app import app
from models import setup_db, Movie, Actor, database_path
from flask import request, _request_ctx_stack, abort


CASTING_ASSISTANT = os.environ["ASSISTANT"]
CASTING_DIRECTOR = os.environ["DIRECTOR"]
EXECUTIVE_PRODUCER = os.environ["PRODUCER"]


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_path = os.environ["DATABASE_URL"]
        self.app.config['TESTING'] = True

        self.new_movie = {
            "title": "Wanted",
            "release_date": "Sun, 02 Feb 2020 00:00:00 GMT"
        }
        self.update_movie = {
            "title": "This movie is updated"
        }
        self.new_actor = {
            "name": "James McAvoy",
            "age": "42",
            "gender": "male"
        }
        self.update_actor = {
            "name": "Name-Updated"
        }
        self.test_movie = {
            "title": "Tom and jerry",
            "release_date": "15-2-2021",
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    # test Movies endpoint
    def test_get_movies(self):
        res = self.client().get(
            '/movies',
            headers={
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER}"
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_create_new_movie(self):
        res = self.client().post(
            '/movies',
            headers={
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER}"
            },
            json=self.new_movie
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie(self):
        res = self.client().delete(
            '/movies/6',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_movie'])

    def test_update_movie(self):
        update_movie = {'title': 'Hello', 'release_date': '2/1/2001'
                        }
        res = self.client().patch(
            '/movies/2',
            json=update_movie,
            headers={"Authorization": f"Bearer {EXECUTIVE_PRODUCER}"}
        )
    
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # test Actors endpoint
    def test_get_actors(self):
        res = self.client().get(
            '/actors',
            headers={
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER}"
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_new_actor(self):
        res = self.client().post(
            '/actors',
            headers={
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER}"
            }, json=self.new_actor
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actor(self):
        create_actor = {
            'name': 'Tom Cruise',
            'age': '30',
            'gender': 'Male'
        }
        res = self.client().post(
            '/actors',
            headers={
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER}"
            },
            json=create_actor
        )
        data = json.loads(res.data)
        actor_id = data['created_actor']['id']
        res = self.client().delete(
            '/actors/{}'.format(actor_id),
            headers={
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER}"
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_delete_actor(self):
        response = self.client().delete(
            '/actors/2',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            data['message'],
            {
                'code': 'no_permission',
                'description': 'No permission'
            }
        )

    def test_update_actor(self):
        updated_actor = {
            "name": "odai",
            "age": 36,
            "gender": "male"
        }
        res = self.client().patch(
            '/actors/1',
            json=updated_actor,
            headers={
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER}"
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['patched_actor'])

    # test RBAC and test for error behavior of each endpoint
    def test_401_get_actors_without_permessions(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_404_get_movie_by_id(self):
        response = self.client().get(
            f"/movies/{2345}",
            headers={"Authorization": f"Bearer {EXECUTIVE_PRODUCER}"}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_401_post_movie(self):
        response = self.client().post(
            "/movies",
            json=self.test_movie,
            headers={"Authorization": f"Bearer {CASTING_ASSISTANT}"},
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(
            data['message'],
            {
                'code': 'no_permission',
                'description': 'No permission'
            }
        )

    def test_404_patch_movie(self):
        response = self.client().patch(
            '/movies/12323',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_401_patch_movie_unauthorized(self):
        response = self.client().patch(
            '/movies/1',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(
            data['message'],
            {
                'code': 'no_permission',
                'description': 'No permission'
            }
        )

    def test_401_delete_movie(self):
        response = self.client().delete(
            '/movies/2',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(
            data['message'],
            {
                'code': 'no_permission',
                'description': 'No permission'
            }
        )

    def test_422_delete_movie(self):
        response = self.client().delete(
            '/movies/22321',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_404_get_actor_by_id(self):
        response = self.client().get(
            '/actors/100',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_401_post_actor_unauthorized(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Mary', 'age': 22, "gender": "female"},
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(
            data['message'],
            {
                'code': 'no_permission',
                'description': 'No permission'
            }
        )

    def test_401_patch_actor_unauthorized(self):
        response = self.client().patch(
            '/actors/1',
            json={'name': 'John', 'age': 25, "gender": "male"},
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(
            data['message'],
            {
                'code': 'no_permission',
                'description': 'No permission'
            }
        )

    def test_404_patch_actor(self):
        response = self.client().patch(
            '/actor/12323',
            json={'name': 'Johnathan', 'age': 25, "gender": "male"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_401_delete_actor(self):
        response = self.client().delete(
            '/actors/2',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            data['message'],
            {
                'code': 'no_permission',
                'description': 'No permission'
            }
        )

    def test_404_delete_actor(self):
        response = self.client().delete(
            '/actors/22321',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

if __name__ == "__main__":
    unittest.main()
