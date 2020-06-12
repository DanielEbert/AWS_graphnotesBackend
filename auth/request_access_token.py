import jwt

import hashlib
import datetime
import boto3


dynamodb = boto3.client('dynamodb')

def request_access_token(event, context):
    headers = event['headers']

    if not 'id' in headers or not 'sessiontoken' in headers:
        return {
            'statusCode': 400,
            'body': "id and sessiontoken required."
        }

    # id and sessiontoken can't be empty
    if not len(headers['id']) or not len(headers['sessiontoken']):
        return {'statusCode': 400, 'body': "id and sessiontoken required."}

    # Hash sessiontoken with sha256
    hashed_session_token = hashlib.sha256(
        headers['sessiontoken'].encode('utf-8')).hexdigest()

    # Authenticate sessiontoken
    db_resp = dynamodb.get_item(
            TableName='sessiontoken', 
            Key={'token':{'S':hashed_session_token}}
        )
    if not 'Item' in db_resp or db_resp['Item']['id']['S'] != headers['id']:
        return {'statusCode': 400, 'body': "Wrong id or sessiontoken."}

    # Generate accesstoken
    payload = {
        'sub': headers['id'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=10),
        'iat': datetime.datetime.utcnow()
    }
    # The access_token is of type bytes in python3. Therefore the bytes are
    # converted to a string and sent back
    access_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return {'statusCode': 200, 'body': access_token.decode('utf-8')}
