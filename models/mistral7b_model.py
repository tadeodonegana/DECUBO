import boto3
import json

class Mistral7b:
    def __init__(self, config):
        self.client = boto3.client(
            'bedrock-runtime',
            aws_access_key_id=config['aws_access_key_id'],
            aws_secret_access_key=config['aws_secret_access_key'],
            region_name=config['aws_region']
        )
        self.model_id = 'mistral.mistral-7b-instruct-v0:2'

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
        
        full_response = ""
        for event in response['body']:
            chunk = event['chunk']['bytes']
            chunk_json = json.loads(chunk.decode('utf-8'))
            if 'outputs' in chunk_json:
                full_response += chunk_json['outputs'][0]['text']
        
        return full_response