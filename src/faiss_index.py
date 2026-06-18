import numpy as np
import faiss

# Load Saved Embeddings
embeddings = np.load("embeddings.npy")

print("Embedding Shape:", embeddings.shape)

# Convert to float32
embeddings = embeddings.astype("float32")

# Create FAISS Index
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

print("Vectors Indexed:", index.ntotal)

# Save Index
faiss.write_index(
    index,
    "researchers.index"
)

print("FAISS Index Saved Successfully")