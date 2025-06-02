import os
import boto3
from botocore.exceptions import ClientError

class S3Service:
    bucket_name = os.environ.get('BUCKET_NAME', 'carddesigner')
    client = boto3.client('s3')

    def upload_file(self, file_content, file_name):
        path = f'public/users/photos/{file_name}'
        # file_content.decode('utf-8', errors='replace')
        print(file_content)
        try:
            response = S3Service.client.put_object(
                Bucket=S3Service.bucket_name,
                Key=path,
                Body=file_content
            )
            # Gera URL pública (ajuste conforme política de acesso)
            url = f"https://{S3Service.bucket_name}.s3.amazonaws.com/{path}"
            return {"success": True, "url": url, "path": path}
        except ClientError as e:
            print(f"Erro ao fazer upload do arquivo {file_name}: {e}")
            return {"success": False, "error": str(e)}
