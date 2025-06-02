import json

class LambdaResponse:
    @staticmethod
    def success(uploaded_files: str, response_body: str) -> dict:
        return {
        'statusCode': 201,
        'headers': {
            'Content-Type': 'application/json',
            'Location': uploaded_files
        },
        'body': json.dumps(response_body)
        }


    @staticmethod
    def bad_request(message: str) -> dict:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": message}),
        }

    @staticmethod
    def forbidden(message: str) -> dict:
        return {
            "statusCode": 403,
            "body": json.dumps({"message": message}),
        }

    @staticmethod
    def not_found(message: str) -> dict:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": message}),
        }

    @staticmethod
    def internal_server_error(message: str) -> dict:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": message}),
        }

    @staticmethod
    def too_many_requests(message: str) -> dict:
        return {
            "statusCode": 429,
            "body": json.dumps({"message": message})
        }
