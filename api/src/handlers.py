def get_health(event, context):
    return {
        'headers': {'Content-Type': 'application/json'},
        'statusCode': 200
    }
