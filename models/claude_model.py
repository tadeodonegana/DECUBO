import boto3
import json

class Claude:
    def __init__(self, config):
        self.client = boto3.client(
            'bedrock-runtime',
            aws_access_key_id=config['aws_access_key_id'],
            aws_secret_access_key=config['aws_secret_access_key'],
            region_name=config['aws_region']
        )
        self.model_id = 'anthropic.claude-v2:1'

    def generate(self, prompt):
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens_to_sample": 512,
            "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
            "temperature": 0.7,
            "top_p": 1
        })
        
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=body
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['completion']