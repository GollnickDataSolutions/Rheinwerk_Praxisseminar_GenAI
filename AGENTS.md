# Repository Guide for AI Assistants

This repository contains course materials for "Generative KI mit Python" (Generative AI with Python).

## Setup & Environment

- **Python Version**: Locked to Python 3.12.* (see `pyproject.toml` and `uv.lock`)
- **Package Management**: Supports both `pip` (via `requirements.txt`) and `uv`
- **Environment Activation**:
  ```bash
  # Windows
  .venv\Scripts\activate
  
  # Mac/Linux
  source .venv/bin/activate
  ```

## Key Commands

### Installation
```bash
# Using pip (traditional)
pip install -r requirements.txt

# Using uv (recommended - faster)
uv sync --link-mode copy

# PyTorch requires special installation (not fully Python 3.13 compatible yet)
pip3 install --pre torch --index-url https://download.pytorch.org/whl/nightly/cpu
```

### Development
- No formal test suite found - scripts are example code for course demonstrations
- No linting or type checking configured
- All executable Python scripts are in `scripts/` and `unsere_skripte/` directories

## Structure

- `scripts/` - Organized course scripts by topic (D01_LLM, D02_VectorDB_RAG, D03_Agents)
- `unsere_skripte/` - Additional working scripts and experiments
- `slides/` - Course presentation materials
- `data/` - Data files for examples (in subdirectories)
- `weltliteratur/` - Literary text data for RAG examples

## Important Notes

- **Environment Variables**: Required API keys (OpenAI, OpenRouter, etc.) must be set in `.env` file
- **PyTorch Compatibility**: PyTorch installation requires special treatment as noted in README
- **No Build/Test Pipeline**: This is a teaching repository, not a production codebase
- **Jupyter-style Cells**: Many scripts use `#%%` cell markers for IDE cell execution (VS Code/PyCharm)

## Working with Scripts

- Most scripts are standalone examples designed to be run independently
- Check for `.env` dependencies before running any script that uses external APIs
- Look for `data/` subdirectories when scripts reference data files
- Scripts use German variable names and comments (course is in German)