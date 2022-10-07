import firebase_admin

from firebase_admin import credentials, auth, firestore, exceptions
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from functools import wraps
from settings import firebaseAdmin_config, flask_config


# Initialize Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = flask_config['SECRET_KEY']
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize Firebase_admin and Pyrebase
cred = credentials.Certificate(firebaseAdmin_config)
firebase = firebase_admin.initialize_app(cred)
db = firestore.client()


def check_token(f):
    """ Ensure we're dealing with a valid authenticated user """
    @wraps(f)
    def wrap(*args,**kwargs):
        data = request.get_json()
        id_token = data.get('id_token')
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
        id_token = data.get('id_token')
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

        return f(*args,**kwargs)
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


@app.route('/api/user/state/<action>', methods=['POST'])
@check_admin_token
def change_account_state(action):
    """ Disable/enable a Firebase User Account """
    if request.method == 'POST':
        data = request.get_json()
        uid = data['uid'] # uid of the user to be enabled/disabled

        try:
            if action == 'disable':
                auth.update_user(uid, disabled=True)
                doc_ref = db.collection('users').document(uid)
                doc_ref.update({'isActive': False})
                response = jsonify({'status': 'success', 'message': 'user disabled'})
            elif action == 'enable':
                auth.update_user(uid, disabled=False)
                doc_ref = db.collection('users').document(uid)
                doc_ref.update({'isActive': True})
                response = jsonify({'status': 'success', 'message': 'user enabled'})
            elif action == 'delete':
                auth.delete_user(uid);
                db.collection('users').document(uid).delete()
                response = jsonify({'status': 'success', 'message': 'user deleted'})
            return response, 200

        except exceptions.FirebaseError as e:
            response = {'status': 'error', 'message': repr(e)}
            return response, 400


@app.route('/api/markers', methods=['POST'])
def get_all_markers():
    """ Fetch all marker data from the database """
    if request.method == 'POST':
        marker_data = []
        try:
            docs = db.collection('mapMarkers').stream()
            for doc in docs:
                marker_data.append(doc.to_dict())
            return marker_data
        except exceptions.FirebaseError as e:
            response = {'status': 'error', 'message': repr(e)}
            return response, 400


@app.route('/api/markers/user/<uid>', methods=['POST'])
@check_token
def get_user_markers(uid):
    """ Fetch all marker data from the database """
    if request.method == 'POST':
        marker_data = []
        try:
            docs = db.collection('mapMarkers').where('uid', '==', uid).stream()
            for doc in docs:
                marker_data.append(doc.to_dict())
            return marker_data
        except exceptions.FirebaseError as e:
            response = {'status': 'error', 'message': repr(e)}
            return response, 400


@app.route('/api/markers/<muid>', methods=['POST'])
@check_token
def get_marker_id(muid):
    """ Fetch all marker data from the database """
    if request.method == 'POST':
        marker_data = []
        try:
            docs = db.collection('mapMarkers').where('muid', '==', muid).stream()
            for doc in docs:
                marker_data.append(doc.to_dict())
            return marker_data
        except exceptions.FirebaseError as e:
            response = {'status': 'error', 'message': repr(e)}
            return response, 400


@app.route('/api/markers/<muid>/downvote', methods=['POST'])
def downvote_marker(muid):
    """ Increment the upvote count by 1 """
    if request.method == 'POST':
        try:
            doc_ref = db.collection('mapMarkers').document(muid)
            doc_ref.update({'downvotes': firestore.Increment(1)})
            response = {'status': 'success', 'message': 'Document updated!'}
            return response, 200
        except exceptions.FirebaseError as e:
            response = {'status': 'error', 'message': repr(e)}
            return response, 400


@app.route('/api/markers/<muid>/hide/<isAdminHidden>', methods=['POST'])
@check_admin_token
def update_marker_visibility(muid, isAdminHidden):
    """ Set marker.isAdminHidden to True of False"""
    if request.method == 'POST':
        try:
            doc_ref = db.collection('mapMarkers').document(muid)
            doc_ref.update({'isAdminHidden': False if isAdminHidden == 'false' else True, 'isVisible': False if isAdminHidden == 'true' else True})
            response = {'status': 'success', 'message': 'Document updated!'}
            return response, 200
        except exceptions.FirebaseError as e:
            response = {'status': 'error', 'message': repr(e)}
            return response, 400