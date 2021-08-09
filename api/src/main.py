def health_get_endpoint(event, context):
    return {
        'headers': {'Content-Type': 'application/json'},
        'statusCode': 200
    }


if __name__ == '__main__':
    pass
