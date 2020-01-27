import json

from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# db_drop_and_create_all()


# ROUTES

@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        drinks = Drink.query.all()

        if not drinks:
            abort(404)

        drinks = [drink.short() for drink in drinks]

        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200

    except Exception as error:
        raise error


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drink_details(jwt):
    try:
        drinks = Drink.query.all()

        if not drinks:
            abort(404)

        drinks = [drink.long() for drink in drinks]

        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200

    except Exception as error:
        raise error


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    try:
        new_drink = request.get_json()

        title = json.loads(request.data)['title']
        if title == '':
            abort(400)

        drink = Drink(
            title=new_drink.get('title'),
            recipe=json.dumps(new_drink.get('recipe'))
        )
        drink.insert()

        return jsonify({
            'success': True,
            'drinks': drink.long()
        }), 201

    except exc.SQLAlchemyError:
        abort(422)
    except Exception as error:
        raise error


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(jwt, drink_id):
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        body = request.get_json()

        if not drink:
            abort(404)

        title = json.loads(request.data)['title']
        if title == '':
            abort(400)
        drink.title = title

        if 'recipe' in body:
            recipe = json.loads(request.data)['recipe']
            if not isinstance(recipe, list):
                abort(400)
            drink.recipe = json.dumps(recipe)

        drink.update()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200

    # except exc.SQLAlchemyError:
    #     abort(422)
    except Exception as error:
        raise error


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, drink_id):
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if not drink:
            abort(404)

        drink.delete()

        return jsonify({
            'success': True,
            'delete': drink_id
        }), 200

    except exc.SQLAlchemyError:
        abort(422)
    except Exception as error:
        raise error


# Error Handling

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": error.description
    }), 404


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': error.description
    }), 401


@app.errorhandler(403)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': error.description
    }), 403


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": error.description
    }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": error.description
    }), 400


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": error.description
    }), 405


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": error.description
    }), 500


@app.errorhandler(AuthError)
def authentication_error(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error
    }), error.status_code
