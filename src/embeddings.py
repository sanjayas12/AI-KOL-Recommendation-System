import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

from database import get_connection

# Database Connection
conn = get_connection()

query = """
SELECT
    author_name,
    institution,
    country,
    paper_count,
    citations,
    h_index,
    concepts    
FROM researcher_profile
"""

df = pd.read_sql(query, conn)

conn.close()

print("Profiles Loaded:", len(df))

# Create Profile Text
texts = []

for _, row in df.iterrows():

    profile_text = f"""
    Author: {row['author_name']}
    Institution: {row['institution']}
    Country: {row['country']}
    Published Papers: {row['paper_count']}
    citations: {row['citations']}
    H index: {row['h_index']}
    Research topics:{row['concepts']}
    """
    texts.append(profile_text)

print("Text Records:", len(texts))

# Load Embedding Model
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(texts)
print("Embedding Shape:", embeddings.shape)

# Save Embeddings
np.save("embeddings.npy",embeddings)

# Save Metadata
df.to_csv("researcher_metadata.csv",index=False)

print("Embeddings saved successfully")
print("Metadata saved successfully")