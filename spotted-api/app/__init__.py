import firebase_admin
import json
import pyrebase
from datetime import datetime, timedelta

import requests.exceptions
from firebase_admin import credentials, auth, firestore, exceptions
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from functools import wraps
from settings import firebase_config, firebaseAdmin_config, flask_config


# Initialize Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = flask_config['SECRET_KEY']
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize Firebase_admin and Pyrebase
cred = credentials.Certificate(firebaseAdmin_config)
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(firebase_config)
db = firestore.client()

# Database Helper functions
from .helpers import username_available


def check_token(f):
    """ Ensure we're dealing with a valid authenticated user """
    @wraps(f)
    def wrap(*args,**kwargs):
        data = request.get_json()
        id_token = data['id_token']
        if not id_token:
            return jsonify({'status': 'error', 'message': 'No token provided'}), 403

        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
        except Exception as e:
            return jsonify({'status': 'error', 'message': 'Invalid token'}), 403

        return f(uid)
    return wrap


def check_admin_token(f):
    """ Ensure the request is coming from an admin user """
    @wraps(f)
    def wrap(*args,**kwargs):
        data = request.get_json()
        id_token = data['id_token']
        if not id_token:
            return jsonify({'status': 'error', 'message': 'No token provided'}), 403

        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            doc_ref = db.collection('users').document(uid)
            doc = doc_ref.get()
            user_data = doc.to_dict()
            if not user_data.get('isAdmin'):
                raise Exception

        except Exception as e:
            return jsonify({'status': 'error', 'message': 'Invalid token'}), 403

        return f()
    return wrap


@app.route('/api/users/list', methods=['POST'])
@check_admin_token
def list_users():
    users_list = []
    # Iterate through all users. This will still retrieve users in batches,
    # buffering no more than 1000 users in memory at a time.
    for user in auth.list_users().iterate_all():
        user = {'uid': user.uid, 'email': user.email, 'displayName': user.display_name, 'isDisabled': user.disabled}
        users_list.append(user)

    return users_list


@app.route('/api/users/disable', methods=['POST'])
@check_admin_token
def disable_account():
    """ Disable a Firebase User Account """
    if request.method == 'POST':
        data = request.get_json()
        disable_uid = data['uid'] # uid of the user to be disabled

        try:
            auth.update_user(disable_uid, disabled=True)
            response = jsonify({'status': 'success', 'message': 'user disabled'})
            return response, 200

        except exceptions.FirebaseError as e:
            response = {'status': 'error', 'message': repr(e)}
            return response, 400
