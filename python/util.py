
def response(statusCode: int, body: str, cors: bool=True) -> dict:
    if cors:
        return {
            'statusCode': statusCode, 
            'body': body,
            'headers': {
                'Access-Control-Allow-Origin': '*' 
            }
        }
    else:
        return {
            'statusCode': statusCode, 
            'body': body
        }