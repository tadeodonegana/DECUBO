import boto3
import json

class Llama370b:
    def __init__(self, config):
        self.client = boto3.client(
            'bedrock-runtime',
            aws_access_key_id=config['aws_access_key_id'],
            aws_secret_access_key=config['aws_secret_access_key'],
            region_name=config['aws_region']
        )
        self.model_id = 'arn:aws:bedrock:us-east-1:901659043704:inference-profile/us.meta.llama3-1-70b-instruct-v1:0'

    def generate(self, prompt):
        body = json.dumps({
            "prompt": prompt,
            "temperature": 0.7,
            "top_p": 1,
            "max_gen_len": 512
        })
        
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=body,
        )
        
        response_body = json.loads(response['body'].read().decode('utf-8'))
        return response_body['generation']