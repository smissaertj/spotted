from app import db

def username_available(username):
    try:
        username_docs = db.collection('users').where('username', '==', username).stream()
        if len(list(username_docs)) > 0:
            response = {'status': 'error', 'message': 'Username is taken.'}
            return response, 400
        response = {'status': 'success', 'message': 'Username is free.'}
        return response, 200
    except Exception as e:
        error = json.loads(e.args[1])['error']
        response = {'status': 'error', 'message': error['message']}
        return response, 400