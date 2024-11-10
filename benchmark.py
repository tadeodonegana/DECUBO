import pandas as pd
import logging
import importlib
from tqdm import tqdm
from utils import load_config, format_prompt, parse_response

def main():
    config = load_config()
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    df = pd.read_csv('DECUBO.csv')
    
    # Initialize and load enabled models
    models = {}
    for model_name, settings in config['models'].items():
        if settings['enabled']:
            try:
                module = importlib.import_module(f"models.{model_name}_model")
                model_class = getattr(module, model_name.capitalize())
                models[model_name] = model_class(config)
                logger.info(f"Initialized model: {model_name}")
            except Exception as e:
                logger.error(f"Failed to initialize model {model_name}: {e}")
    
    results = []
    prompt_template = config['prompt_template']
    
    # Benchmark loop
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        prompt_text = row['prompt']
        correct_answer = row['Answer'].strip().upper()
        
        for model_name, model in models.items():
            formatted_prompt = format_prompt(prompt_text, prompt_template)
            try:
                response = model.generate(formatted_prompt)
                model_answer = parse_response(response)
                is_correct = model_answer == correct_answer
                result = {
                    'question_id': idx,
                    'model_name': model_name,
                    'model_answer': model_answer,
                    'correct_answer': correct_answer,
                    'is_correct': is_correct
                }
                results.append(result)
            except Exception as e:
                logger.error(f"Error with model {model_name} on question {idx}: {e}")
                result = {
                    'question_id': idx,
                    'model_name': model_name,
                    'model_answer': None,
                    'correct_answer': correct_answer,
                    'is_correct': False,
                    'error': str(e)
                }
                results.append(result)
    
    # Save results
    results_df = pd.DataFrame(results)
    results_df.to_csv('benchmark_results.csv', index=False)
    logger.info("Benchmarking complete. Results saved to 'benchmark_results.csv'.")

if __name__ == '__main__':
    main()
