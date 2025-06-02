import base64
import json
from requests_toolbelt.multipart import decoder

class ProcessFiles:

    @staticmethod
    def process(event):
        body = base64.b64decode(event['body']) if event.get('isBase64Encoded') else event['body']
        content_type = event['headers'].get('Content-Type') or event['headers'].get('content-type')

        multipart_data = decoder.MultipartDecoder(
            body if isinstance(body, bytes) else body.encode(),
            content_type
        )

        files = {}

        for part in multipart_data.parts:
            content_disposition = part.headers.get(b'Content-Disposition', b'').decode()
            name = None
            filename = None

            for item in content_disposition.split(';'):
                item = item.strip()
                if item.startswith('name='):
                    name = item.split('=')[1].strip('"')
                elif item.startswith('filename='):
                    filename = item.split('=')[1].strip('"')

            if filename:
                files[name] = {
                    'filename': filename,
                    'content_type': part.headers.get(b'Content-Type', b'').decode(),
                    'size': len(part.content),
                    'content': part.content
                }

        return files
