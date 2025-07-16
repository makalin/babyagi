# BabyAGI: Exploring Artificial General Intelligence

## Description
BabyAGI is an open-source project designed to explore the foundations of Artificial General Intelligence (AGI) through a simplified, task-driven framework. It uses large language models (LLMs) to autonomously generate, prioritize, and execute tasks, mimicking aspects of general intelligence such as reasoning, planning, and adaptability. Built in Python, BabyAGI leverages libraries like LangChain for task orchestration and local LLMs for privacy-focused reasoning, making it an accessible platform for researchers and developers interested in AGI.

The project’s goal is to provide a lightweight, experimental environment for studying AGI concepts, with a focus on iterative task management and self-improving workflows. BabyAGI is not a full AGI system but a stepping stone for exploring how autonomous agents can learn and operate in dynamic environments.

## Features
- **Task Automation**: Generates, prioritizes, and executes tasks based on user-defined objectives.
- **Local LLM Integration**: Supports privacy-focused operation with models like Llama or Hugging Face transformers.
- **Extensible Framework**: Easily customizable for experimenting with new AGI concepts or integrating with other tools.
- **Vector Storage**: Uses Pinecone or local vector databases for task and context management.
- **Pluggable Tool System**: Agent can invoke a wide range of tools for web, data, math, file, and AI tasks.
- **Community-Driven**: Open to contributions for advancing AGI research.

## Pluggable Tools
BabyAGI includes a powerful tool system. The agent can invoke tools by outputting lines like:
```
TOOL: tool_name: argument
```

### Available Tools (selected examples)
- **Web & Data**: `web_search`, `web_scrape`, `wikipedia_search`, `url_fetch`, `html_title_extractor`
- **Files**: `file_read`, `write_file`, `csv_reader`, `pdf_text_extractor`, `image_to_text`, `zip_file_creator`
- **Math & Text**: `math_calculator`, `summarize_text`, `extract_entities`, `json_validator`, `unit_converter`, `palindrome_checker`, `anagram_finder`, `sha256_hasher`, `rot13_encoder`, `caesar_cipher`, `morse_code_encoder`
- **AI & Images**: `ai_image_generate`, `image_generation`, `plot_data`
- **System & Utility**: `shell_command`, `timer_sleep`, `current_datetime`, `random_number`, `uuid_generator`, `password_generator`
- **Network & APIs**: `http_status_checker`, `ip_geolocation`, `url_shortener`, `database_query`, `send_email`, `weather_info`, `currency_converter`
- **Other**: `prime_number_checker`, `fibonacci_calculator`, `markdown_to_html`

> **Note:** Some tools require optional dependencies:
> - `plot_data`: `matplotlib`
> - `web_scrape`: `beautifulsoup4`
> - `markdown_to_html`: `markdown`
> - `pdf_text_extractor`, `image_to_text`: stubs (can be extended)

### Example Tool Usage
The agent may output:
```
TOOL: web_search: "LangChain Python documentation"
TOOL: plot_data: "1,2,3::4,5,6::Sample Plot"
TOOL: database_query: "mydb.sqlite::SELECT * FROM users"
TOOL: ai_image_generate: "A futuristic city skyline at sunset"
```

## Installation
To get started with BabyAGI, follow these steps:

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/makalin/babyagi.git
   cd babyagi
   ```

2. **Install Dependencies**:
   BabyAGI requires Python 3.8+. Install dependencies using:
   ```sh
   pip install -r requirements.txt
   ```
   For optional tool support:
   ```sh
   pip install matplotlib beautifulsoup4 markdown
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file with your LLM and vector storage credentials (e.g., Pinecone API key or local model path). Example:
   ```plaintext
   LLM_MODEL_PATH=/path/to/local/llm
   PINECONE_API_KEY=your-pinecone-key
   ```

4. **Run BabyAGI**:
   Start the task loop with:
   ```sh
   python babyagi.py --objective "Your research or automation goal"
   ```

## Usage
BabyAGI operates by initializing with an objective, then iteratively generating, prioritizing, and executing tasks. Example workflow:

1. **Set Objective**:
   Define a goal, e.g., "Research sustainable energy solutions."
   ```sh
   python babyagi.py --objective "Research sustainable energy solutions"
   ```

2. **Task Loop**:
   BabyAGI will:
   - Generate tasks (e.g., "Search for solar panel efficiency data").
   - Prioritize tasks based on relevance and urgency.
   - Execute tasks using LLM-driven reasoning or external tools (see Pluggable Tools).
   - Store results in a vector database for context retention.

3. **Monitor Output**:
   Check the terminal or log files for task progress and results.

Example:
```
> python babyagi.py --objective "Plan a community garden"
[INFO] Task 1: Research local soil conditions
[INFO] Task 2: Identify suitable plants for the region
[INFO] Executing: Research local soil conditions...
[OUTPUT] Soil pH range: 6.0-7.0, suitable for most vegetables
[INFO] Executing: TOOL: web_search: "best vegetables for acidic soil"
[OUTPUT] Web search for 'best vegetables for acidic soil' completed. (HTML content omitted)
```

## Configuration
Customize BabyAGI by modifying `config.yaml`:
```yaml
llm:
  model: "local-llm"
  max_tokens: 512
task_manager:
  max_tasks: 10
  prioritization: "relevance"
vector_store:
  provider: "pinecone"
  index: "babyagi-tasks"
  embedding_model: "all-MiniLM-L6-v2"
```

## Contributing
We welcome contributions to advance AGI research! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [LangChain](https://github.com/hwchase17/langchain) for task orchestration.
- [Hugging Face Transformers](https://github.com/huggingface/transformers) for local LLM support.
- [Pinecone](https://www.pinecone.io/) for vector storage.
- Inspired by early AGI research and autonomous agent frameworks.
