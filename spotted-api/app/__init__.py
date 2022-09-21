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


@app.route('/api/signup', methods=['POST'])
def signup():
    """ Handle Firebase account creation """
    content_type = request.headers.get('Content-Type')

    if request.method == 'POST':
        if content_type == 'application/json':
            data = request.get_json()
            email = data['email']
            passwd = data['password']
            username = data['username']

            try:
                user = pb.auth().create_user_with_email_and_password(email, passwd)
                user_id = user['localId']
                user_data = { 'username': username, 'email': email }
                db.collection('users').document(user_id).set(user_data)
                response = {'status': 'success', 'message': 'Check your inbox for the activation link.'}
                return response, 200
            except Exception as e:
                error = json.loads(e.args[1])['error']
                if error['message'] == 'EMAIL_EXISTS':
                    response = {'status': 'error', 'message': 'Email already registered.'}
                else:
                    response = {'status': 'error', 'message': error['message']}
                return response, 400


@app.route('/api/signup/check_username', methods=['POST'])
def check_username():
    """ Check if the username is available """
    content_type = request.headers.get('Content-Type')

    if request.method == 'POST':
        if content_type == 'application/json':
            data = request.get_json()
            username = data['username']
            response = username_available(username)
            return response


@app.route('/api/login', methods=['POST'])
def login():
    """ Handle the login request with Firebase """
    if request.method == 'POST':
        data = request.get_json()
        email = data['email']
        password = data['password']
        expires_in = timedelta(hours=1)

        try:
            user = pb.auth().sign_in_with_email_and_password(email, password)
            id_token = user['idToken']
            session_cookie = auth.create_session_cookie(id_token, expires_in=expires_in)
            expires = datetime.now() + expires_in
            response = jsonify({'status': 'success', 'message': 'Logged in!', 'id_token': id_token})
            response.set_cookie('spottedSession', session_cookie, expires=expires, httponly=True, secure=True)
            return response

        except Exception as e:
            print(e)
            error = json.loads(e.args[1])['error']
            if error['message'] == 'INVALID_PASSWORD' or error['message'] == 'EMAIL_NOT_FOUND':
                response = jsonify({ 'status': 'error', 'message': 'Email or Password invalid!'})
            else:
                response = jsonify({'status': 'error', 'message': error['message']})
            return response, 401


@app.route('/api/logout', methods=['GET'])
def logout():
    """ Expire the session cookie, logging out the user """
    session_cookie = request.cookies.get('spottedSession')
    if session_cookie:
        response = jsonify({'status': 'success', 'message': 'Logged out!'})
        response.set_cookie('spottedSession', expires=0)
        return response


@app.route('/api/private')
@check_token
def private(user):
    """ Show user details if session cookie auth token is valid """
    return user
