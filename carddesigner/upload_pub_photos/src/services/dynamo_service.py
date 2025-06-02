import boto3
from botocore.exceptions import ClientError

client = boto3.resource('dynamodb')
table = client.Table('carddesigner')

class DynamoService:
    @staticmethod
    def safe_photo(sub, photo_name):
        try:
            response = table.update_item(
                Key={"sub": sub},
                UpdateExpression="""
                    SET
                        n_uploads = if_not_exists(n_uploads, :zero) + :inc,
                        uploads = list_append(if_not_exists(uploads, :empty_list), :new_photo)
                """,
                ExpressionAttributeValues={
                    ':zero': 0,
                    ':inc': 1,
                    ':empty_list': [],
                    ':new_photo': [photo_name]
                },
                ReturnValues="ALL_NEW"
            )
            return response['Attributes']
        except ClientError as err:
            print(f"Erro ao atualizar o perfil do usuário - {err}")
            raise err

    @staticmethod
    def count_uploads(sub, photos_len):
        try:
            response = table.get_item(Key={"sub": sub})
            n_uploads = response['Item'].get('n_uploads', 0)
            return ((n_uploads + photos_len) >= 5)
        except ClientError as err:
            print(f"Erro ao buscar o perfil do usuário - {err}")
            raise err
