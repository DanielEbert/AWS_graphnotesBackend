import jwt

SECRET_KEY = "7ba933c6a65cc9f786e7d50b7aa97ad6b5a4220d77880a2db974bf49d7ed1554"


def authenticate_user_with_token(access_token: str) -> str:
    try:
        token = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')
        return token["sub"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    return None


def authenticate_user_with_event(event: dict) -> str:
    headers = event['headers']

    if not 'Authorization' in headers:
        return None

    authorization_header = headers['Authorization'].split()

    if len(authorization_header) != 2:
        return None
    if authorization_header[0] != "Bearer":
        return None

    return authenticate_user_with_token(authorization_header[1])


# Return authenticated id or empty string
def authenticate(access_token: str=None, event: dict=None) -> str:
    if access_token != None:
        return authenticate_user_with_token(access_token)
    elif event != None:
        return authenticate_user_with_event(event)
    return None