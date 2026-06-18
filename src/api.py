from fastapi import FastAPI
import requests
import numpy as np
import pandas as pd
import faiss
from sklearn.preprocessing import MinMaxScaler

from sentence_transformers import SentenceTransformer

app = FastAPI(title="KOL Recommendation API")

# Load Once During Startup
index = faiss.read_index("researchers.index")
metadata = pd.read_csv("researcher_metadata.csv")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("API Loaded Successfully")

@app.get("/")
def home():

    return {"message": "KOL Recommendation API Running"}

@app.get("/search")
def search(query: str):

    query_embedding = model.encode(
        [query]
    )

    query_embedding = np.array(query_embedding,dtype="float32")

    distances, indices = index.search(query_embedding,k=5)

    results = []

    for rank, idx in enumerate(indices[0],start=1):

        researcher = metadata.iloc[idx]

        results.append(
            {
                "rank": rank,
                "author_name":researcher["author_name"],
                "institution":researcher["institution"],
                "country":researcher["country"],
                "paper_count":int(researcher["paper_count"]),
                "citations": (int(researcher["citations"]) if pd.notna(researcher["citations"])else 0),
                "h_index": (int(researcher["h_index"])if pd.notna(researcher["h_index"]) else 0),
                "research_topics": (researcher["concepts"] if pd.notna(researcher["concepts"]) else "")
            }
        )

    return {"query": query,"results": results}

@app.post("/recommend")
def recommend(query:str):

    query_embedding = model.encode([query])

    query_embedding = np.array(query_embedding,dtype="float32")
    distance, indices = index.search(query_embedding,k=5)
    top_idx = indices[0][0]
    researcher = metadata.iloc[top_idx]

    return {
        "query": query,
        "recommended_researcher": researcher["author_name"],
        "institution": researcher["institution"],
        "country": researcher["country"],
        "paper_count": int(researcher["paper_count"]),
        "citations": int(researcher["citations"]) if pd.notna(researcher["citations"]) else 0,
        "h_index": int(researcher["h_index"]) if pd.notna(researcher["h_index"]) else 0,
        "research_topics": researcher["concepts"] if pd.notna(researcher["concepts"]) else ""
    }

@app.post("/ai-recommend")
def ai_recommend(query: str):

    # Convert Query to Embedding
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding, dtype="float32")

    # Get Top 5 Similar Researchers
    distances, indices = index.search(
        query_embedding,
        k=5
    )

    recommendations = []

    # Build Top 5 Recommendations
    for idx in indices[0]:

        researcher = metadata.iloc[idx]

        recommendations.append(
            {
                "author_name": researcher["author_name"],
                "institution": researcher["institution"],
                "country": researcher["country"],
                "paper_count": int(researcher["paper_count"])
                if pd.notna(researcher["paper_count"]) else 0,

                "citations": int(researcher["citations"])
                if pd.notna(researcher["citations"]) else 0,

                "h_index": int(researcher["h_index"])
                if pd.notna(researcher["h_index"]) else 0,

                "research_topics": researcher["concepts"]
                if pd.notna(researcher["concepts"]) else ""
            }
        )

    # Top Researcher
    top_idx = indices[0][0]
    top_researcher = metadata.iloc[top_idx]

    prompt = f"""
    You are an AI KOL Recommendation Assistant.

    Query:
    {query}

    Researcher Details:

    Name: {top_researcher['author_name']}
    Institution: {top_researcher['institution']}
    Country: {top_researcher['country']}
    Citations: {top_researcher['citations']}
    H Index: {top_researcher['h_index']}
    Research Topics: {top_researcher['concepts']}

    Explain in 4-5 professional lines why this researcher should be recommended.
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3:mini",
            "prompt": prompt,
            "stream": False
        }
    )

    ai_summary = response.json()["response"]

    return {
        "query": query,
        "top_researcher": top_researcher["author_name"],
        "ai_summary": ai_summary,
        "recommendations": recommendations
    }

@app.post("/ai-recommend-v2")
def ai_recommend_v2(query: str):

    # Query Embedding
    query_embedding = model.encode([query])

    query_embedding = np.array(
        query_embedding,
        dtype="float32"
    )

    # Retrieve Top 20 Candidates
    distances, indices = index.search(
        query_embedding,
        k=20
    )

    candidate_df = metadata.iloc[
        indices[0]
    ].copy()

    # Handle Null Values
    candidate_df["citations"] = (
        candidate_df["citations"].fillna(0)
    )

    candidate_df["h_index"] = (
        candidate_df["h_index"].fillna(0)
    )

    # Preserve Original Values
    candidate_df["original_citations"] = (
        candidate_df["citations"]
    )

    candidate_df["original_h_index"] = (
        candidate_df["h_index"]
    )

    # Normalize Citation + H Index
    scaler = MinMaxScaler()

    candidate_df[
        ["citations", "h_index"]
    ] = scaler.fit_transform(
        candidate_df[
            ["citations", "h_index"]
        ]
    )

    # Similarity Score
    candidate_df["similarity_score"] = [
        float(
            1 / (float(distance) + 1)
        )
        for distance in distances[0]
    ]

    # Hybrid Ranking Formula
    candidate_df["final_score"] = (
        0.7 * candidate_df["similarity_score"]
        +
        0.2 * candidate_df["citations"]
        +
        0.1 * candidate_df["h_index"]
    )

    # Sort by Final Score
    candidate_df = candidate_df.sort_values(
        by="final_score",
        ascending=False
    )

    # Top Researcher
    top_researcher = candidate_df.iloc[0]

    # Build Recommendation List
    recommendations = []

    for _, researcher in candidate_df.head(5).iterrows():

        recommendations.append(
            {
                "author_name": researcher["author_name"],
                "citations": int(
                    researcher["original_citations"]
                ),
                "h_index": int(
                    researcher["original_h_index"]
                ),
                "similarity_score": round(
                    float(
                        researcher["similarity_score"]
                    ),
                    4
                ),
                "final_score": round(
                    float(
                        researcher["final_score"]
                    ),
                    4
                )
            }
        )

    # LLM Prompt
    prompt = f"""
    You are an AI KOL Recommendation Assistant.

    Research Domain:
    {query}

    Researcher Details:

    Name: {top_researcher['author_name']}
    Institution: {top_researcher['institution']}
    Country: {top_researcher['country']}
    Citations: {int(top_researcher['original_citations'])}
    H Index: {int(top_researcher['original_h_index'])}
    Research Topics: {top_researcher['concepts']}

    Explain in 4-5 professional lines why this researcher is a strong recommendation for this research domain.
    Focus on expertise, research impact, citations and domain relevance.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3:mini",
            "prompt": prompt,
            "stream": False
        }
    )

    ai_summary = response.json()["response"]

    return {
        "query": query,
        "top_researcher": top_researcher["author_name"],
        "citations": int(
            top_researcher["original_citations"]
        ),
        "h_index": int(
            top_researcher["original_h_index"]
        ),
        "ai_summary": ai_summary,
        "recommendations": recommendations
    }