import boto3
import json

class Llama:
    def __init__(self, config):
        self.client = boto3.client(
            'bedrock-runtime',
            aws_access_key_id=config['aws_access_key_id'],
            aws_secret_access_key=config['aws_secret_access_key'],
            region_name=config['aws_region']
        )
        self.model_id = 'meta.llama2-70b-chat-v1'

    def generate(self, prompt):
        body = json.dumps({
            "prompt": prompt,
            "max_tokens": 512,
            "temperature": 0.7,
            "top_p": 1
        })
        
        response = self.client.invoke_model_with_response_stream(
            modelId=self.model_id,
            body=body
        )
        
        response_body = b''
        for event in response['body']:
            chunk = event['chunk']['bytes']
            response_body += chunk
            
        result = json.loads(response_body.decode('utf-8'))
        return result['completion']