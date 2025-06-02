import json
import base64
from io import BytesIO
from requests_toolbelt.multipart import decoder
from src.use_case import UseCase
def lambda_handler(event, context):
    use_case = UseCase(event)
    return use_case.process()
