# AI-Powered KOL Recommendation System

## Overview

The AI-Powered KOL (Key Opinion Leader) Recommendation System helps identify influential researchers in a given research domain using Semantic Search, Vector Databases, Hybrid Ranking, and Generative AI.

The system collects researcher data from OpenAlex, stores researcher profiles in PostgreSQL, generates embeddings using Sentence Transformers, performs semantic similarity search using FAISS, ranks researchers using a hybrid scoring mechanism, and generates AI-powered explanations using Phi3 Mini running locally through Ollama.

---

## Features

* Semantic Search for researchers
* FAISS Vector Similarity Search
* Hybrid Ranking Engine
* AI-generated recommendation explanations
* FastAPI Backend APIs
* Streamlit Interactive Dashboard
* Local LLM Integration using Ollama and Phi3 Mini

---

## Architecture

```text
OpenAlex API
      │
      ▼
PostgreSQL Database
      │
      ▼
Researcher Profiles
      │
      ▼
Sentence Transformers
(all-MiniLM-L6-v2)
      │
      ▼
Embeddings
      │
      ▼
FAISS Vector Index
      │
      ▼
Hybrid Ranking Engine
      │
      ▼
Phi3 Mini (Ollama)
      │
      ▼
FastAPI
      │
      ▼
Streamlit Dashboard
```

---

## Technology Stack

### Data Collection

* OpenAlex API

### Database

* PostgreSQL

### Machine Learning

* Sentence Transformers
* all-MiniLM-L6-v2

### Vector Database

* FAISS

### Generative AI

* Ollama
* Phi3 Mini

### Backend

* FastAPI

### Frontend

* Streamlit

### Language

* Python

---

## Hybrid Ranking Formula

Researchers are ranked using:

```text
Final Score =
0.7 × Similarity Score
+
0.2 × Citation Score
+
0.1 × H-Index Score
```

This ensures recommendations are relevant, influential, and academically impactful.

---

## Project Workflow

### Step 1: Data Collection

Research papers and author information are collected from OpenAlex.

### Step 2: Researcher Profile Creation

Profiles contain:

* Author Name
* Institution
* Country
* Paper Count
* Citations
* H-Index
* Research Topics

### Step 3: Embedding Generation

Researcher profiles are converted into embeddings using Sentence Transformers.

### Step 4: Semantic Search

FAISS retrieves researchers with the highest semantic similarity to the user's query.

### Step 5: Hybrid Ranking

Researchers are ranked using similarity score, citation score, and h-index score.

### Step 6: AI Recommendation

Phi3 Mini generates a natural language explanation describing why the researcher is recommended.

---

## Dashboard Preview

### Streamlit Dashboard

Add screenshot here:

```text
screenshots/streamlit_dashboard.png
```

### API Response

Add screenshot here:

```text
screenshots/swagger_response.png
```

---

## Example Query

Input:

```text
Computer Vision
```

Output:

```text
Top Researcher:
Pushmeet Kohli

Citations:
119631

H Index:
101
```

---

## Future Enhancements

* Researcher Comparison Dashboard
* Citation Network Analysis
* Research Trend Detection
* Docker Deployment
* Cloud Deployment
* Advanced LLM Recommendations
* Multi-Domain Expert Discovery

---

## Learning Outcomes

This project provided hands-on experience with:

* Semantic Search
* Vector Databases (FAISS)
* Embedding Models
* Retrieval Systems
* Generative AI Integration
* FastAPI Development
* Streamlit Dashboard Development
* PostgreSQL Database Design
* End-to-End AI System Architecture

---

## Author

**Sanjay A.S.**

Data Engineer | Data Science & Generative AI Enthusiast
