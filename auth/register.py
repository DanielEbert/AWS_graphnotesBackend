from argon2 import PasswordHasher
from util import response

import boto3
import json


dynamodb = boto3.client('dynamodb')

def register(event, context):
    try:
        sent = json.loads(event['body'])
    except:
        return response(400, 'Error parsing sent body.')

    if not 'id' in sent or not 'pw' in sent:
        return response(400, 'id and pw required.')

    # id and pw can't be empty
    if not len(sent['id']) or not len(sent['pw']):
        return response(400, 'id and pw required.')

    # User is registered only if id doesn't exist already
    if 'Item' in dynamodb.get_item(
                TableName='user', 
                Key={'id':{'S':sent['id']}}
            ):
        return response(400, 'id exists already.')

    # Hash pw with argon2
    try :
        hasher = PasswordHasher()
        hashed_pw = hasher.hash(sent['pw'])
    except:
        return response(400, 'Hashing pw failed.')

    # Save [id, hashed_pw] in user db
    dynamodb.put_item(
        TableName='user',
        Item={
            'id':{'S':sent['id']},
            'pw':{'S':hashed_pw}
        }
    )

    return {'statusCode': 200}