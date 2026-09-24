import os
from flask import (Flask, request, abort, jsonify, render_template)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie, rollback
from auth import requires_auth, AuthError
from flask_migrate import Migrate


def create_app(test_config=None):

    # create and configure the app

    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type, Authorization, true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS'
        )
        response.headers.add('Access-Control-Allow-origins', '*')
        return response

    # create the actors action here
    @app.route('/', methods=['GET'])
    def start():
        return "<h1> This is my Final Project :) </h1>"

    # Get actors

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(jwt):
        # Get all actors route
        actors = Actor.query.all()

        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors],
        }), 200

    # get the actorst by_id

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor(jwt, actor_id):
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)

        return jsonify({
            "success": True,
            "actor": actor.format()
        }), 200

    # post actor

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actors(jwt):
        body = request.get_json()

        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')

        if (name is None) or (age is None) or (gender is None):
            abort(422)
        try:
            new_actor = Actor(
                name=name,
                gender=gender,
                age=age
            )

            new_actor.insert()
        except Exception:
            abort(500)

        return jsonify({
            "success": True,
            "created_actor": new_actor.format()
        }), 200

    # patch the data

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actors(jwt, actor_id):
        body = request.get_json()

        actor = Actor.query.get(actor_id)

        if actor is None:
            abort(404)

        new_name = body.get('name')
        new_age = body.get('age')
        new_gender = body.get('gender')

        if (new_name is None) or (new_age is None) or (new_gender is None):
            abort(422)

        try:
            if new_name is not None:
                actor.name = new_name
            if new_age is not None:
                actor.age = new_age
            if new_gender is not None:
                actor.gender = new_gender

            actor.update()
        except:
            rollback()
            abort(422)

        return jsonify({
            "success": True,
            "patched_actor": actor.format()
        }), 200

    # get the actor by id

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(jwt, actor_id):
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)

        try:
            actor.delete()
            return jsonify({
                "success": True,
                "deleted_actor": actor.format()
            }), 200

        except Exception:
            rollback()
            abort(500)

    # Get movie

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(jwt):
        movies = Movie.query.all()

        return jsonify({
            "success": True,
            "movies": [movie.format() for movie in movies]
        })

    # Get movie by id

    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie(jwt, movie_id):
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)
        return jsonify({
            "success": True,
            "movie": [movie.format()]
        })

    # Create movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movies(jwt):

        body = request.get_json()
        title = body.get('title')
        release_date = body.get('release_date')

        if title is None or release_date is None:
            abort(400)

        try:
            new_movie = Movie()
            new_movie.title = title
            new_movie.release_date = release_date

            new_movie.insert()

        except Exception as e:
            print(e)

        return jsonify({
                'success': True,
                'created_movie': new_movie.format()
            }), 200

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movies(jwt, id):

        movie = Movie.query.get(id)

        if movie is None:
            abort(404)

        body = request.get_json()

        title = body.get("title")
        release_date = body.get("release_date")

        if (title is None) or (release_date is None):
            abort(422)

        try:
            if title is not None:
                movie.title = title

            if release_date is not None:
                movie.relaese_date = release_date

            movie.update()

            return jsonify({
                "success": True,
                "patched_movie": movie.format()
            }), 200

        except Exception:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE', "GET"])
    @requires_auth('delete:movie')
    def delete_movie(jwt, movie_id):
        try:
            movie = Movie.query.filter(
                Movie.id == movie_id
            ).one_or_none()

            if movie is None:
                abort(404)

            movie.delete()

            return jsonify({
                'success': True,
                'deleted_movie': movie.format()
            }), 200

        except:
            rollback()
            abort(422)

# Handle error

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'Bad request'
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden"
        }), 403

    @app.errorhandler(404)
    def resource_not_found_error(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": 'Unprocessable'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    return app

app = create_app()
