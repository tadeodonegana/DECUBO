import pandas as pd
import logging
import importlib
from tqdm import tqdm
from utils import load_config, format_prompt, parse_response
from time import sleep
from random import uniform
import os

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
    
    results_file = 'benchmark_results.csv'
    if os.path.exists(results_file):
        results_df = pd.read_csv(results_file)
        processed = set(zip(results_df['question_id'], results_df['model_name']))
        logger.info(f"Loaded existing results. {len(processed)} entries found.")
    else:
        processed = set()
    
    prompt_template = config['prompt_template']
    
    # Benchmark loop
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        prompt_text = row['prompt']
        correct_answer = row['Answer'].strip().upper()
        
        for model_name, model in models.items():
            # Check if this question and model have already been processed
            if (idx, model_name) in processed:
                continue
            
            formatted_prompt = format_prompt(prompt_text, prompt_template)
            max_retries = 5
            base_delay = 1
            
            for attempt in range(max_retries):
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
                    # Write result to CSV file in append mode
                    result_df = pd.DataFrame([result])
                    if not os.path.exists(results_file):
                        result_df.to_csv(results_file, index=False)
                    else:
                        result_df.to_csv(results_file, mode='a', header=False, index=False)
                    # Update processed set
                    processed.add((idx, model_name))
                    break  # Success, exit retry loop
                        
                except Exception as e:
                    if 'ThrottlingException' in str(e) and attempt < max_retries - 1:
                        # Base delay of 60 seconds (1 minute), leading to delays of ~1min, 2min, 4min, 8min, 16min
                        base_delay = 60  
                        delay = base_delay * (2 ** attempt) + uniform(0, 30)
                        logger.warning(f"Rate limit hit for {model_name}, waiting {delay/60:.1f} minutes before retry {attempt + 1}/{max_retries}")
                        sleep(delay)
                        continue
                        
                    # If we've exhausted retries or it's a different error, log and continue
                    logger.error(f"Error with model {model_name} on question {idx}: {e}")
                    result = {
                        'question_id': idx,
                        'model_name': model_name,
                        'model_answer': None,
                        'correct_answer': correct_answer,
                        'is_correct': False,
                        'error': str(e)
                    }
                    # Write result with error to CSV
                    result_df = pd.DataFrame([result])
                    if not os.path.exists(results_file):
                        result_df.to_csv(results_file, index=False)
                    else:
                        result_df.to_csv(results_file, mode='a', header=False, index=False)
                    # Update processed set
                    processed.add((idx, model_name))
                    break
    logger.info("Benchmarking complete. Results saved to 'benchmark_results.csv'.")

if __name__ == '__main__':
    main()
