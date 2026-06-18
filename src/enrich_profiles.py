import requests
from database import get_connection

# Database Connection
conn = get_connection()
cursor = conn.cursor()

# Get Top Researchers First
cursor.execute("""
SELECT id, author_name
FROM researcher_profile
WHERE citations IS NULL
ORDER BY paper_count DESC
LIMIT 5000
""")

researchers = cursor.fetchall()

total = len(researchers)

print(f"Researchers Found: {total}")

for count, researcher in enumerate(researchers, start=1):

    researcher_id = researcher[0]
    author_name = researcher[1]

    print(f"{count}/{total} - Processing: {author_name}")

    try:

        url = "https://api.openalex.org/authors"

        params = {
            "search": author_name,
            "per-page": 1
        }

        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        if response.status_code != 200:
            print(f"API Error: {author_name}")
            continue

        data = response.json()

        results = data.get("results", [])

        if not results:
            print(f"No Match Found: {author_name}")
            continue

        author = results[0]

        citations = author.get(
            "cited_by_count",
            0
        )

        h_index = (
            author.get(
                "summary_stats",
                {}
            ).get(
                "h_index",
                0
            )
        )

        topics = []

        if author.get("topics"):

            topics = [
                topic["display_name"]
                for topic in author["topics"][:5]
            ]

        concepts = ", ".join(topics)

        cursor.execute("""
        UPDATE researcher_profile
        SET
            citations = %s,
            h_index = %s,
            concepts = %s
        WHERE id = %s
        """,
        (
            citations,
            h_index,
            concepts,
            researcher_id
        ))

    except Exception as e:

        print(f"Error Processing: {author_name}")
        print(e)

# Commit Once
conn.commit()

cursor.close()
conn.close()

print("\nProfile Enrichment Completed") 