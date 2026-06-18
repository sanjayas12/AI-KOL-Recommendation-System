from database import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
truncate table researcher_profile;               
""")

#aggregation authors
cursor.execute("""
insert into researcher_profile
(
author_name,
institution,
country,
paper_count)
select author_name,
               max(institution) as institution,
               max(country) as country,
               count(*) as paper_count
               from authors
               group by author_name
               
               """)

conn.commit()
cursor.close()
conn.close()