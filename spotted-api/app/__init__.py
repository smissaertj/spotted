import firebase_admin
import json
import pyrebase
from datetime import datetime, timedelta

import requests.exceptions
from firebase_admin import credentials, auth, firestore
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
    """ Verify the validity of the Firebase Auth Token stored in the session cookie """
    @wraps(f)
    def wrap(*args,**kwargs):
        session_cookie = request.cookies.get('spottedSession')
        if not session_cookie:
            return jsonify({'status': 'error', 'message': 'No token provided'}), 400

        try:
            user = auth.verify_session_cookie(session_cookie, check_revoked=True)
        except Exception as e:
            return jsonify({'status': 'error', 'message': 'Invalid token.'}), 400

        return f(user)
    return wrap


@app.route('/api/users/list', methods=['POST'])
def list_users():
    pass


@app.route('/api/users/disable', methods=['POST'])
def disable_account():
    """ Disable a Firebase User Account """
    if request.method == 'POST':
        data = request.get_json()
        uid = data['uid']

        try:
            auth.update_user(uid, disabled=True)
            response = jsonify({'status': 'success', 'message': 'user disable'})
            return response

        except Exception as e:
            error = json.loads(e.args[1])['error']
            print(e)
            response = jsonify({'status': 'error', 'message': error['message']})
            return response, 401

