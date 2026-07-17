# GenAi-practise
This repo is used to practise genai concepts

RAG:

RAG (Retrieval-Augmented Generation) improves LLM responses by retrieving the most relevant information from a vector database before generating an answer.
The user query is converted into embeddings, matched with similar documents, and the retrieved context is sent to the LLM to produce an accurate response.

![RAG Architecture](RAG/rag-flow.png)

Langchain Flow

LangChain simplifies building LLM applications by connecting prompts, models, parsers, and other components into a single workflow.

![Langchain-flow](RAG/langchain/Initial-langchain-flow.png)

Mostly used OLLAMA
# Ollama Setup Guide for Local GenAI & RAG

## Overview

This project uses **Ollama** to run Large Language Models (LLMs) and Embedding Models locally without relying on cloud APIs.

---

# Architecture

```
                +---------------------+
                |     Ollama Server   |
                | localhost:11434     |
                +----------+----------+
                           |
          +----------------+----------------+
          |                                 |
   Embedding Model                   LLM Model
 (nomic-embed-text)                     (llama3)
          |                                 |
          +----------------+----------------+
                           |
                     LangChain
                           |
                    Chroma Vector DB
```

---

# 1. Install Ollama

Download Ollama from the official website:

https://ollama.com/download

Install it normally.

---

# Verify Installation

Open a terminal.

```bash
ollama --version
```

Example:

```
ollama version is 0.31.2
```

---

# Verify Ollama Server

Normally the Ollama server starts automatically.

Check:

```bash
ollama list
```

If it returns:

```
NAME                       ID              SIZE      MODIFIED     
llama3:latest              365c0bd3c000    4.7 GB    2 weeks ago 
```

The server is running but no models have been downloaded.

If you receive

```
connection refused
```

start the server:

```bash
ollama serve
```

If you receive

```
Only one usage of each socket address...
```

ignore it.

It means the server is already running.

---

# Download Embedding Model

This project uses

```
nomic-embed-text
```

Install it:

```bash
ollama pull nomic-embed-text
```

Verify:

```bash
ollama list
```

Expected:

```
NAME                       ID              SIZE      MODIFIED      
nomic-embed-text:latest    0a109f422b47    274 MB    8 minutes ago    
llama3:latest              365c0bd3c000    4.7 GB    2 weeks ago      
```

#  Local REST API

Default endpoint

```
http://localhost:11434

```

---

## List Installed Models

```
GET

http://localhost:11434/api/tags

```
---

# Common Commands

```
ollama --version
ollama list
ollama ps
ollama serve
ollama run MODEL
ollama pull MODEL
ollama rm MODEL
ollama show MODEL
```

---

# Recommended Open Source Models

## Embeddings

```
nomic-embed-text
```

# Ingestion pipeline 
"""
 document -> Load -> split -> embedding -> storevdb
"""
# Query pipeline
"""
question -> embedding -> query vdb(retriver) -> prompt builder (context + query) llm  -> output
"""