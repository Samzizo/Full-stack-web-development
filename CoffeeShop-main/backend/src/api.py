import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"/*": {"origins": "*"}})

# initialize the datbase

db_drop_and_create_all()

# CORS headers


@app.after_request
def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type,Authorization,true'
    )
    response.headers.add(
        'Access-Control-Allow-Methods',
        'GET,PUT,POST,DELETE,PATCH'
    )
    return response

drink = Drink(
    title='black coffee',
    recipe='[{"name":"beans","color":"red","parts":1}]'
)
drink.insert()
drink = Drink(
    title='latte',
    recipe='[{"name":"milk and beans", "color":"green","parts":2}]'
)
drink.insert()
drink = Drink(
    title='double expresso',
    recipe='[{"name":"only beans","color":"blue","parts":3}]'
)
drink.insert()

# ROUTES

# GET /drinks


@app.route('/drinks', methods=['GET'])
def get_drinks():                       # public endpoint
    all_drinks = Drink.query.all()
    drinks = [drink.short() for drink in all_drinks]

    if not all_drinks:
        abort(404)

    return jsonify({
        'success': True,
        'drinks': drinks
    }), 200


# GET /drinks-detail
# require the 'get:drinks-detail' permission


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    try:
        all_drinks = Drink.query.all()

        if all_drinks is None:
            abort(404)

        drinks = [drink.long() for drink in all_drinks]

        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200

    except Exception as e:
        print('Error while doing something:', e)
        traceback.print_exc()


# POST /drinks
# require the 'post:drinks' permission


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(jwt):

    drink = request.get_json()
    new_title = drink.get('title', None)
    new_recipe = drink.get('recipe', None)

    new_drink = Drink(
        title=new_title,
        recipe=json.dumps(new_recipe)
    )

    try:
        new_drink.insert()

        return jsonify({
            'success': True,
            'drinks': new_drink.long()
        }), 200

    except Exception as e:
        print(e)


# PATCH /drinks/<id>
# require the 'patch:drinks' permission


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(jwt, drink_id):
    data = request.get_json()
    title = data.get('title', None)
    recipe = data.get('recipe', None)

    try:
        drink = Drink.query.filter_by(
            id=drink_id
        ).one_or_none()
        if drink is None:
            abort(404)

        if title is None:
            abort(400)

        if title is not None:
            drink.title = title

        if recipe is not None:
            drink.recipe = json.dumps(recipe)

        drink.update()

        updated_drink = Drink.query.filter_by(
            id=drink_id
        ).first()

        return jsonify({
            'success': True,
            'drinks': [updated_drink.long()]
        })
    except:
        abort(422)


# DELETE /drinks/<id>
# require the 'delete:drinks' permission

@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, drink_id):
    try:
        drink = Drink.query.filter(
            Drink.id == drink_id
        ).one_or_none()

        if not drink:
            abort(404)

        drink.delete()

        return jsonify({
            'success': True,
            'delete': drink_id
        }), 200

    except Exception as error:
        raise error


# Error Handling


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
    }), 500
