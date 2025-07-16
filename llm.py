import os
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

class LLM:
    def __init__(self, model_path, max_tokens=512):
        self.model_path = model_path
        self.max_tokens = max_tokens
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path)
        self.generator = pipeline('text-generation', model=self.model, tokenizer=self.tokenizer)

    def generate(self, prompt):
        result = self.generator(prompt, max_length=self.max_tokens, num_return_sequences=1)
        return result[0]['generated_text'] 