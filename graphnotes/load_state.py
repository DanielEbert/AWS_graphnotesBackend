from authenticate import authenticate

import boto3


dynamodb = boto3.client('dynamodb')

def load_state(event, context):
    user = authenticate(event=event)
    if user is None:
        return {'statusCode': 401}

    # Load id's data from graphnotes db 
    db_resp = dynamodb.get_item(
            TableName='graphnotes', 
            Key={'id':{'S':user}}
        )

    data = '{}'
    if 'Item' in db_resp:
        data = db_resp['Item']['data']['S']

    return {'statusCode': 200, 'body': data}