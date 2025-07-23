# airepo
projects with ai integrated features and functionality

## Introduction
This repo has multiple projects which are having ai integration. It might be a supporting project without ai integration as well.

## General Setup

Create a virtual environment for setting up the dependencies and python modules. This will be mostly one time setup. If anything wrong happens, remove the current venv and follow these instructions again.

Navigate to the repo home page and activate the virtual environment.

```
cd <REPO HOME DIR>
python3 -m venv lc-agent-env
source lc-agent-env/bin/activate
```

Install the below dependencies within the venv
```
pip install langchain langchain-core
pip install langchain-google-genai
pip install python-dotenv
```
