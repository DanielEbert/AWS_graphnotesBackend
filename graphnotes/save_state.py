from authenticate import authenticate

import boto3


dynamodb = boto3.client('dynamodb')

def save_state(event, context):
    user = authenticate(event=event)
    if user is None:
        return {'statusCode': 401}
    
    data = event['body']

    # Save [id, data] in graphnotes db
    dynamodb.put_item(
        TableName='graphnotes',
        Item={
            'id':{'S':"Test"},
            'data':{'S':data}
        }
    )

    return {'statusCode': 200}