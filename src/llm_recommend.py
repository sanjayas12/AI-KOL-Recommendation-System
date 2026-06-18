import requests

researcher = {
    "author_name": "Joan Lasenby",
    "institution": "University of Cambridge",
    "country": "GB",
    "citations": 1200,
    "h_index": 18,
    "concepts": "Computer Vision, Machine Learning, Image Analysis"
}

prompt = f"""
you are an AI KOL Recommendation assistance

Researcher Details:

Name: {researcher['author_name']}
Institution: {researcher['institution']}
COuntry: {researcher['country']}
Citations : {researcher['citations']}
H index: {researcher['h_index']}
Research Topics: {researcher['concepts']}

Explain in 4-5 professional lines why this researcher should be recommended.
"""

response = requests.post(
    "http://localhost:11434/api/generate",
    json = {
        "model": "phi3:mini",
        "prompt": prompt,
        "stream" : False
    }
)
result = response.json()
print(result["response"])