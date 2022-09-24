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
    """ Verify the validity of the Firebase JWT token """
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


@app.route('/api/users/list', methods=['POST'])
def list_users():
    pass


@app.route('/api/users/disable', methods=['POST'])
@check_token
def disable_account():
    """ Disable a Firebase User Account """
    if request.method == 'POST':
        data = request.get_json()
        requester_uid = data.get('admin_uid') # uid of the user making the request
        disable_uid = data['uid'] # uid of the user to be disabled

        try:
            # Check if the request is coming from an admin user
            doc_ref = db.collection('users').document(requester_uid)
            doc = doc_ref.get()
            if doc.exists:
                requester_user_data = doc.to_dict()

                if requester_user_data.get('isAdmin'):
                    auth.update_user(disable_uid, disabled=True)
                    response = jsonify({'status': 'success', 'message': 'user disabled'})
                    return response, 200
                else:
                    response = jsonify({'status': 'error', 'message': 'Forbidden'})
                    return response, 403

            else:
                raise auth.UserNotFoundError('requester_uid does not exist')

        except exceptions.FirebaseError as e:
            response = {'status': 'error', 'message': repr(e)}
            return response, 400
