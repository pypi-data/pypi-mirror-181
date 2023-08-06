import os
import json
import logging as _logging

from cryptography.fernet import Fernet as _Fernet
import jwt as _jwt

_logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s', level=_logging.INFO)
_log = _logging.getLogger(__name__)

class BadTokenException(Exception):
    pass

class NoTokenException(Exception):
    pass

class BadDataObjectException(Exception):
    pass

class DataNotSerializableException(Exception):
    """
    Data must be one of dict, list, str, int, float, bool, None
    """

def create_sso_token() -> bytes:
    """
    !!! This returns a secret !!!

    SSO token needs to be compatible with a Fernet key.
    Fernet key must be 32 url-safe base64-encoded bytes. 
    This method does not write the key to any place but simply returns it. 
    """
    return _Fernet.generate_key()

def check_sso_token(sso_token: str) -> None:
    """
    Check to see if the token is Fernet compatible.
    """
    try:
        _  = _Fernet(sso_token)
    except Exception as e:
        raise BadTokenException("SSO Token is not compatible.")

def get_sso_token_from_file():
    try:
        with open(f"/run/secrets/sso_token", 'r') as f:
            sso_token = f.read()
    except:
        _log.warning("SSO Token file could not be read. Checking for custom env path...")

        try:
            token_path = os.environ.get('OPENSARLAB_SSO_TOKEN_PATH', '')
            if not token_path:
                raise Exception("Environment variable 'OPENSARLAB_SSO_TOKEN_PATH' not found.")
            with open(f"{token_path}", 'r') as f:
                sso_token = f.read()
        except Exception as e: 
            _log.error(f"Alternative SSO token file could not be read: {e}")
            raise

    if not sso_token:
        _log.error("No SSO Token can be found.")
        raise NoTokenException()

    return sso_token.strip()

def encrypt(data, sso_token: str=None) -> str:
    if not sso_token:
        sso_token = get_sso_token_from_file()
    check_sso_token(sso_token)

    if not isinstance(data, (dict, list, str, int, float, bool, None)):
        raise DataNotSerializableException()

    try:
        payload = {"data": data}
    except Exception as e:
        raise BadDataObjectException()

    encoded_jwt = _jwt.encode(payload=payload, key=sso_token, algorithm="HS256")
    try:
        bytes_encoded_jwt = encoded_jwt.encode('ascii')
    except:
        bytes_encoded_jwt = encoded_jwt
    cipher_suite = _Fernet(sso_token)
    bytes_encrypted_jwt = cipher_suite.encrypt(bytes_encoded_jwt)
    encrypted_jwt = bytes_encrypted_jwt.decode('ascii')
    return encrypted_jwt

def decrypt(encrypted_jwt: str, sso_token: str=None) -> str:
    if not sso_token:
        sso_token = get_sso_token_from_file()
    check_sso_token(sso_token)

    try:
        bytes_encrypted_jwt = encrypted_jwt.encode('ascii')
    except:
        bytes_encrypted_jwt = encrypted_jwt
    cipher_suite = _Fernet(sso_token)
    bytes_encoded_jwt = cipher_suite.decrypt(bytes_encrypted_jwt)
    payload = _jwt.decode(jwt=bytes_encoded_jwt, key=sso_token, algorithms=["HS256"])

    try:
        data = payload['data']
    except Exception as e:
        raise BadDataObjectException()

    return data
