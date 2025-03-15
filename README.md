# IEA_Plugin

## Introduction

Hi, this is IEA_Plugin version 1.0.

## Setup

### Python version

Please ensure you're using Python 3.11 or later. 
This version is required for optimal compatibility with LangGraph. If you're on an older version, 
upgrading will ensure everything runs smoothly.
```
python3 --version
```

### Clone repo
```
git clone https://github.com/University-of-CA-Santa-Barbara-IEA-Lab/IEA_Plugin.git
$ cd IEA_Plugin
```

### Create an environment and install dependencies
#### Mac/Linux/WSL
```
$ python3 -m venv your-env-name
$ source your-env-name/bin/activate
$ pip install -r requirements.txt
```
#### Windows Powershell
```
PS> python3 -m venv your-env-name
PS> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
PS> your-env-name\scripts\activate
PS> pip install -r requirements.txt
```

### Set OpenAI API key
* If you don't have an OpenAI API key, you can sign up [here](https://openai.com/index/openai-api/).
*  Set `OPENAI_API_KEY` in your environment 

### Sign up and Set LangSmith API
* Sign up for LangSmith [here](https://smith.langchain.com/), find out more about LangSmith
* and how to use it within your workflow [here](https://www.langchain.com/langsmith), and relevant library [docs](https://docs.smith.langchain.com/)!
*  Set `LANGCHAIN_API_KEY`, `LANGCHAIN_TRACING_V2=true` in your environment 

### Set Up Pinecone API for Vector Database Operations

* Pinecone is used for vector database operations.
* You can sign up for an API key [here](https://www.pinecone.io/). 
* Set `PINECONE_API_KEY` in your environment.

### Set up LangGraph Studio

* Currently, Studio only has macOS support and needs Docker Desktop running.
* Download the latest `.dmg` file [here](https://github.com/langchain-ai/langgraph-studio?tab=readme-ov-file#download)
* Install Docker desktop for Mac [here](https://docs.docker.com/engine/install/)

### Running Studio
Graphs for LangGraph Studio are in the `IEA_Plugin/IEA_Agent/` folders.

* To use Studio, you will need to create a .env file with the relevant API keys
