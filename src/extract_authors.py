import requests
from database import get_connection

# OpenAlex Works API
url = "https://api.openalex.org/works"

params = {
    "search": "Artificial Intelligence",
    "per-page": 200
}

# API Request
response = requests.get(url, params=params,timeout = 30)
print("Status Code:", response.status_code)

if response.status_code != 200:
    print("Openlax api error")
    print(response.text)
    exit()

data = response.json()
print("Total Results:", len(data["results"]))

# Database Connection
conn = get_connection()
cursor = conn.cursor()

# Loop through papers
for paper in data["results"]:

    paper_title = paper.get("display_name", "")

    print(f"\nPaper: {paper_title}")

    authorships = paper.get("authorships", [])

    for author in authorships:

        author_name = (
            author.get("author", {})
            .get("display_name", "")
        )

        institution = ""

        if author.get("institutions"):
            institution = (
                author["institutions"][0]
                .get("display_name", "")
            )

        country = ""

        if author.get("institutions"):
            country = (
                author["institutions"][0]
                .get("country_code", "")
            )

        print(
            author_name,
            "|",
            institution,
            "|",
            country
        )

        cursor.execute("""
            INSERT INTO authors
            (
                author_name,
                institution,
                country,
                paper_title
            )
            VALUES (%s,%s,%s,%s)
        """,
        (
            author_name,
            institution,
            country,
            paper_title
        ))


conn.commit()
cursor.close()
conn.close()

print("\nAuthors data loaded successfully")