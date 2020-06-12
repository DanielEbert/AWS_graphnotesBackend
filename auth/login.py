from argon2 import PasswordHasher

import secrets
import hashlib
import boto3


dynamodb = boto3.client('dynamodb')

def login(event, context):
    try:
        sent = json.loads(event['body'])
    except:
        return {'statusCode': 400, 'body': "Failed parsing json body."}

    if not 'id' in sent or not 'pw' in sent:
        return {'statusCode': 400, 'body': "id and pw required."}

    # id and pw can't be empty
    if not len(sent['id']) or not len(sent['pw']):
        return {'statusCode': 400, 'body': "id and pw required."}

    # Check if user exists
    db_resp = dynamodb.get_item(
            TableName='user', 
            Key={'id':{'S':sent['id']}}
        )
    if not 'Item' in db_resp:
        return {'statusCode': 400, 'body': "No such id."}

    # Verify pw
    hasher = PasswordHasher()
    try :
        hasher.verify(db_resp['Item']['pw']['S'], sent['pw'])
    except:
        return {'statusCode': 400, 'body': "Wrong Password."}

    # Generate 256 bit sessiontoken
    session_token = secrets.token_hex(32)
    hashed_session_token = hashlib.sha256(
        session_token.encode('utf-8')).hexdigest()

    # Save [hashed_session_token, id] in sessiontoken db
    dynamodb.put_item(
        TableName='sessiontoken',
        Item={
            'token':{'S':hashed_session_token},
            'id':{'S':sent['id']}
        }
    )

    # Return session_token
    return {'statusCode': 200, 'body': session_token}