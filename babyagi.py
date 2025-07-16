import argparse
import os
import yaml
from dotenv import load_dotenv
from llm import LLM
from vector_store import VectorStore
from task_manager import TaskManager


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="BabyAGI: Exploring Artificial General Intelligence")
    parser.add_argument('--objective', type=str, required=True, help='Objective for the agent')
    args = parser.parse_args()

    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    # LLM setup
    llm_model_path = os.getenv('LLM_MODEL_PATH', config['llm']['model'])
    llm_max_tokens = config['llm'].get('max_tokens', 512)
    llm = LLM(llm_model_path, max_tokens=llm_max_tokens)

    # Vector store setup
    vector_cfg = config['vector_store']
    provider = vector_cfg.get('provider', 'local')
    index = vector_cfg.get('index', 'babyagi-tasks')
    pinecone_api_key = os.getenv('PINECONE_API_KEY')
    embedding_model_name = vector_cfg.get('embedding_model', 'all-MiniLM-L6-v2')
    vector_store = VectorStore(provider, index, api_key=pinecone_api_key, embedding_model_name=embedding_model_name)

    # Task manager
    max_tasks = config['task_manager'].get('max_tasks', 10)
    task_manager = TaskManager(llm, vector_store, max_tasks=max_tasks)

    # Run loop
    print(f"[INFO] Starting BabyAGI with objective: {args.objective}")
    task_manager.run_loop(args.objective)

if __name__ == '__main__':
    main() 