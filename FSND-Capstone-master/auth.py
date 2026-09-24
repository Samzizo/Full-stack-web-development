import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from flask import abort
import os

# setup.sh
AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
ALGORITHMS = os.environ.get('ALGORITHMS')
API_AUDIENCE = os.environ.get('API_AUDIENCE')

# AuthError Exception


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

# Get the header from the request

def get_token_auth_header():
    if "Authorization" not in request.headers:
        abort(401)

    auth = request.headers.get('Authorization', None)

    if not auth:
        # raise an AuthError if no header is present
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorizaion header is excepted'
               }, 401)

    # raise an AuthError if the header is malformed
    spliting = auth.split(' ')
    if spliting[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not Found'
                    }, 401)

    elif len(spliting) != 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not Found'
                    }, 401)

    elif len(spliting) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization must be bearer Token'
                     }, 401)

    # return the token part of the header
    token = spliting[1]
    print()
    return token

# check_permissions(permission, payload) method


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
                'code': 'permissions_header_missing',
                'description': 'Permission header missing'
            }, 400)
    if permission not in payload['permissions']:
        raise AuthError({
                'code': 'no_permission',
                'description': 'No permission'
            }, 401)
    return True

# verify_decode_jwt(token) method


def verify_decode_jwt(token):
    jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims Check the audience and issuer'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

# @requires_auth(permission) decorator method


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt = get_token_auth_header()

            try:
                payload = verify_decode_jwt(jwt)

            except:
                abort(401)
            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
