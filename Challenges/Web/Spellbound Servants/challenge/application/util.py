# แก้ไข utils.py ให้เขียน debug ลงไฟล์
import os, pickle, base64
from flask import jsonify, abort, session, request
from functools import wraps
import datetime

generate = lambda x: os.urandom(x).hex()
key = generate(50)

def debug_log(message):
    """เขียน debug message ลงไฟล์"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('/app/application/static/debug.log', 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
        f.flush()

def response(message):
    return jsonify({'message': message})

def isAuthenticated(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.cookies.get('auth', False)

        debug_log(f"[AUTH] Received request to {request.endpoint}")
        
        if not token:
            debug_log("[AUTH] No token found")
            return abort(401, 'Unauthorised access detected!')
        
        debug_log(f"[AUTH] Token received: {token[:50]}...")
        
        try:
            user = pickle.loads(base64.urlsafe_b64decode(token))
            debug_log(f"[AUTH] Successfully deserialized user: {user}")
            debug_log(f"[AUTH] User type: {type(user)}")
            
            kwargs['user'] = user
            result = f(*args, **kwargs)
            debug_log(f"[AUTH] Request completed successfully")
            return result
            
        except Exception as e:
            debug_log(f"[AUTH] Deserialization error: {str(e)}")
            debug_log(f"[AUTH] Error type: {type(e)}")
            return abort(401, 'Unauthorised access detected!')

    return decorator