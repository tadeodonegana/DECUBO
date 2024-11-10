import yaml
import re

def load_config(config_file='config.yaml'):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

def format_prompt(prompt_text, template):
    return template.format(prompt=prompt_text)

def parse_response(response):
    match = re.search(r'\b[A-D]\b', response.upper())
    if match:
        return match.group(0)
    else:
        return None
