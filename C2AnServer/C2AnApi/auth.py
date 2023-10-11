from flask import blueprints, jsonify, abort, request
from hashlib import sha256
from secrets import token_urlsafe

import db

auth = blueprints.Blueprint('auth', __name__)

# definging login_required decorator

def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.get_json()['token']
        if token == None or not db.get_user_by_token(token):
            abort(401)
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@auth.route('/', methods=['POST'])
@auth.route('/getToken/', methods=['POST'])
def getAuthToken():

    user = request.get_json['username']
    password_hash = request.get_json['password_hash']

    if db.check_username_password(user, password_hash):
        return jsonify({'token': db.get_user_token(user)})
    else:
        abort(401)