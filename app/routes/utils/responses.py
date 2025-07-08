from flask import jsonify


def error_response(message, status_code=400):
    return jsonify({'error': message}), status_code


def success_response(data=None, message: str = None, status_code: int = 200):
    response = {}
    if data is not None:
        response['data'] = data
    if message:
        response['message'] = message
    return jsonify(response), status_code
