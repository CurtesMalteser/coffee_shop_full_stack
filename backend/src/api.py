from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES

@app.route("/drinks")
def get_drinks():
    '''
    @TODO implement endpoint error handling
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
    '''
    try:
        drinks = Drink.query.order_by(Drink.id).all()
        drinks = [drink.long() for drink in drinks]    
        return jsonify({
            "success": True,
            "drinks": drinks
        })
    except Exception as e:
        abort(404, e)


@app.route("/drinks-detail")
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    '''
    @TODO implement endpoint
        GET /drinks-detail
            it should require the 'get:drinks-detail' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
            where drinks is the list of drinks
            or appropriate status code indicating reason for failure
    '''
    try:
        print(payload)
        drinks = Drink.query.order_by(Drink.id).all()
        drinks = [drink.long() for drink in drinks]
        return jsonify({
            "success": True,
            "drinks": drinks
        })

    except Exception as e:
        abort(404, e)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    '''
    @TODO implement endpoint
        POST /drinks
            it should create a new row in the drinks table
            it should require the 'post:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink}
            where drink an array containing only the newly created drink
            or appropriate status code indicating reason for failure
    '''

    print(payload)

    try:
        body = request.get_json()
        drink = Drink(
            title=body.get('title'),
            recipe=json.dumps(body.get('recipe'))
        )

        drink.insert()

        return jsonify({
                "success": True,
                "drinks": drink.long()
            })

    except Exception as e:
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id: int):
    '''
    @TODO implement endpoint
        PATCH /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink}
            where drink an array containing only the updated drink
            or appropriate status code indicating reason for failure
    '''
    print(payload)

    try:
        drink = Drink.query.get(drink_id)

        if drink is None:
            abort(404, "Drink not found")
        
        body = request.get_json()
        drink.title=body.get('title')
        drink.recipe=json.dumps(body.get('recipe'))
        drink.update()

        return jsonify({
                "success": True,
                "drinks": drink.long()
            })

    except Exception:
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id: int):
    '''
    @TODO implement endpoint
        DELETE /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "delete": id}
            where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''
    print(payload)

    try:
        drink = Drink.query.get(drink_id)

        drink.delete()

        return jsonify({
                "success": True,
                "delete": drink_id
            })

    except Exception:
        abort(404)


def json_error(error, code):
    '''
    @TODO implement error handlers using the @app.errorhandler(error) decorator
        each error handler should return (with approprate messages):
                jsonify({
                        "success": False,
                        "error": 404,
                        "message": "resource not found"
                        }), 404

    '''
    return jsonify({
        "success": False, 
        "error": code,
        "message": error,
        }), code


# Error Handling
@app.errorhandler(422)
def unprocessable(error):
    '''
    Example error handling for unprocessable entity
    '''
    print(error)
    return json_error("unprocessable", 422)


@app.errorhandler(404)
def not_found(error):
    '''
    @TODO implement error handler for 404
        error handler should conform to general task above
    '''
    print(error)
    return json_error("Not found", 404)


@app.errorhandler(AuthError)
def auth_error(error):
    '''
    @TODO implement error handler for AuthError
    error handler should conform to general task above
    '''
    code = error.status_code
    return json_error(error.error['description'], code)
