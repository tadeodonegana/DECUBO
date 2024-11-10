import openai

class Gpt4:
    def __init__(self, config):
        self.client = openai.OpenAI(api_key=config['openai_api_key'])

    def generate(self, prompt):
        response = self.client.chat.completions.create(
            model='gpt-4',
            messages=[
                {'role': 'user', 'content': prompt}
            ]
        )
        return response.choices[0].message.content