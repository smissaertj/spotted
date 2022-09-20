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
CORS(app)


# Initialize Firebase_admin and Pyrebase
cred = credentials.Certificate(firebaseAdmin_config)
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(firebase_config)
db = firestore.client()


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


@app.route('/signup', methods=['POST'])
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
                # Check if username exists
                username_docs = db.collection('users').where('username', '==', username).stream()
                if len(list(username_docs)) > 0:
                    response = {'status': 'error', 'message': 'Username is taken.'}
                    return response
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


@app.route('/signup/check_username', methods=['POST'])
def check_username():
    """ Handle Firebase account creation """
    content_type = request.headers.get('Content-Type')

    if request.method == 'POST':
        if content_type == 'application/json':
            data = request.get_json()
            username = data['username']

            try:
                username_docs = db.collection('users').where('username', '==', username).stream()
                if len(list(username_docs)) > 0:
                    response = {'status': 'error', 'message': 'Username is taken.'}
                    return response, 400
                response = {'status': 'success', 'message': 'Username is free.'}
                return response
            except Exception as e:
                error = json.loads(e.args[1])['error']
                if error['message'] == 'EMAIL_EXISTS':
                    response = {'status': 'error', 'message': 'Email already registered.'}
                else:
                    response = {'status': 'error', 'message': error['message']}
                return response, 400


@app.route('/login', methods=['POST'])
def login():
    """ Handle the login request with Firebase """
    if request.method == 'POST':
        email = request.form.get('email')
        passwd = request.form.get('password')
        expires_in = timedelta(hours=1)

        try:
            user = pb.auth().sign_in_with_email_and_password(email, passwd)
            id_token = user['idToken']
            session_cookie = auth.create_session_cookie(id_token, expires_in=expires_in)
            response = jsonify({'status': 'success', 'message': 'Logged in! Check user details on /private endpoint. /logout to log out.'})
            expires = datetime.now() + expires_in
            response.set_cookie('spottedSession', session_cookie, expires=expires, httponly=True, secure=True)
            return response

        except Exception as e:
            response = { 'status': 'error', 'message': 'Email or Password invalid!'}
            return render_template('index.html', response=response)


@app.route('/logout', methods=['GET'])
def logout():
    """ Expire the session cookie, logging out the user """
    session_cookie = request.cookies.get('fbSession')
    if session_cookie:
        response = jsonify({'status': 'success', 'message': 'Logged out!'})
        response.set_cookie('fbSession', expires=0)
        return response


@app.route('/private')
@check_token
def private(user):
    """ Show user details if session cookie auth token is valid """
    return user
