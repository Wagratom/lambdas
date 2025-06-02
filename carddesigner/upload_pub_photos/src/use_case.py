# use_case.py
import json
from src.services.s3_service import S3Service
from src.services.dynamo_service import DynamoService
from src.services.process_files import ProcessFiles
from src.service.jwt_service import JwtService
from src.domain.jwt_exceptions import jwtException
from src.domain.lambda_response import LambdaResponse

class UseCase:

    def __init__(self, event):
        self.event = event
        self.s3_service = S3Service()

    def process(self):
        try:
            jwt_token = self.event["headers"]["authorization"]
            sub = self.jwt_service.decode_jwt(jwt_token)

            files = ProcessFiles.process(self.event)

            if DynamoService.count_uploads(sub, len(files)):
                return LambdaResponse.too_many_requests("Usuário sem créditos suficientes limit 5")

            uploaded_files = []
            for name, file_info in files.items():
                file_content = file_info['content']
                file_name = file_info['filename'].replace(' ', '_')

                upload_result = self.s3_service.upload_file(file_content, file_name)

                if upload_result['success']:
                    DynamoService.safe_photo(sub, file_name)
                    uploaded_files.append({
                        'field_name': name,
                        'filename': file_name,
                        'url': upload_result['url']
                    })

            response_body = {
                'message': 'Arquivos recebidos',
                'files': uploaded_files
            }

            uploaded_files = uploaded_files[0]['url'] if uploaded_files else ''
            return LambdaResponse.success(uploaded_files, response_body)

            except jwtException as je:
                return LambdaResponse.forbidden(f"Erro com o token de autorizaçao: {str(je)}")
