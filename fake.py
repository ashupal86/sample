import sqlite3
import mistune
import random
from datetime import datetime

# Create a markdown to HTML converter
markdown = mistune.create_markdown()

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('static/POSTS/Post_2024_12.db')
cursor = conn.cursor()

# Create the posts table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY,
    post_title TEXT,
    post_content TEXT,
    post_author TEXT,
    tags TEXT
)
''')

# Sample data (titles, authors, and tags)
sample_titles = [
    "How to Learn Python",
    "Exploring Data Science",
    "Introduction to Web Development",
    "Mastering Algorithms",
    "Understanding Machine Learning",
    "Python Web Scraping Guide",
    "Deep Dive into Flask",
    "Django for Beginners",
    "Building APIs with Python",
    "Understanding Databases",
    "Getting Started with SQL",
    "Learning Cloud Computing",
    "Building Web Apps with React",
    "Data Visualization Techniques",
    "Advanced Python Programming",
    "Python for Automation",
    "Understanding Cybersecurity",
    "Machine Learning Algorithms",
    "Artificial Intelligence for Everyone",
    "Exploring the Internet of Things"
]

sample_authors = ["John Doe", "Jane Smith", "Alice Johnson", "Bob Brown", "Charlie Green"]
sample_tags = ["Python", "Machine Learning", "Web Development", "Data Science", "AI", "Cloud", "Automation"]

# List of random image URLs (real, high-quality images from Unsplash)
image_urls = [
    "https://images.unsplash.com/photo-1606754535044-320f13d5c034?crop=entropy&cs=tinysrgb&fit=max&ixid=MnwzNjcwMHwwfDF8c2VhcmNofDQyfHxQeXRob258ZW58MHx8fHwxNjc1NzMyNjEy&ixlib=rb-1.2.1&q=80&w=1080",
    "https://images.unsplash.com/photo-1521747116042-5e9b3418b8b2?crop=entropy&cs=tinysrgb&fit=max&ixid=MnwzNjcwMHwwfDF8c2VhcmNofDJ8fGJhdGVyeXxlbnwwfHx8fDE2NzU3MzI3NjM&ixlib=rb-1.2.1&q=80&w=1080",
    "https://images.unsplash.com/photo-1593642532973-d31b6557fa68?crop=entropy&cs=tinysrgb&fit=max&ixid=MnwzNjcwMHwwfDF8c2VhcmNofDk2fHxQeXRob258ZW58MHx8fHwxNjc1NzMyNzI4&ixlib=rb-1.2.1&q=80&w=1080",
    "https://images.unsplash.com/photo-1560296820-4b3501f8f378?crop=entropy&cs=tinysrgb&fit=max&ixid=MnwzNjcwMHwwfDF8c2VhcmNofDQ2fHxkYXRhJTIwc2NpZW5jZXxlbnwwfHx8fDE2NzU3MzI3NzQ&ixlib=rb-1.2.1&q=80&w=1080",
    "https://images.unsplash.com/photo-1498576961412-0bb496ca7558?crop=entropy&cs=tinysrgb&fit=max&ixid=MnwzNjcwMHwwfDF8c2VhcmNofDQyfHxkYXRhJTIwc2NpeWVuY2V8ZW58MHx8fHwxNjc1NzMyNzYy&ixlib=rb-1.2.1&q=80&w=1080",
    "https://images.unsplash.com/photo-1505751170152-8e87a1694b25?crop=entropy&cs=tinysrgb&fit=max&ixid=MnwzNjcwMHwwfDF8c2VhcmNofDQ3fHxkYXRhJTIwc2NpeWVuY2V8ZW58MHx8fHwxNjc1NzMzMDg3&ixlib=rb-1.2.1&q=80&w=1080",
    "https://images.unsplash.com/photo-1519002086231-dc54b8b5cf96?crop=entropy&cs=tinysrgb&fit=max&ixid=MnwzNjcwMHwwfDF8c2VhcmNofDE3fHxjbG91ZCUyMGNvbXB1dGVyfGVufDB8fHx8fDE2NzU3MzI4ODg&ixlib=rb-1.2.1&q=80&w=1080",
    "https://images.unsplash.com/photo-1573497163057-ef6e244e462b?crop=entropy&cs=tinysrgb&fit=max&ixid=MnwzNjcwMHwwfDF8c2VhcmNofDJ8fHByb2dyYW1taW5nfGVufDB8fHx8fDE2NzU3MzMwODg&ixlib=rb-1.2.1&q=80&w=1080",
    "https://images.unsplash.com/photo-1506748686214-b5a376ddc13c?crop=entropy&cs=tinysrgb&fit=max&ixid=MnwzNjcwMHwwfDF8c2VhcmNofDN8fGxvZ29zdWl0ZSUyMGFsaWdufGVufDB8fHx8fDE2NzU3MzMwOTQ&ixlib=rb-1.2.1&q=80&w=1080",
    "https://images.unsplash.com/photo-1560243887-66c3a7b01ba0?crop=entropy&cs=tinysrgb&fit=max&ixid=MnwzNjcwMHwwfDF8c2VhcmNofDJ8fHByb2dyYW1taW5nJTIwY29tcHV0ZXJ8ZW58MHx8fHwxNjc1NzMzMTE2&ixlib=rb-1.2.1&q=80&w=1080"
]

# Function to create Markdown content with random image URL and link
def generate_markdown_content(title):
    image_url = random.choice(image_urls)  # Randomly select an image URL
    link_url = "https://example.com"  # Replace with actual link
    return f"""
# {title}

This is a sample post about **{title}**.

![Image]({image_url})

- Point 1: Introduction to the topic
- Point 2: Why it's important
- Point 3: How to get started

For more details, check out [this link]({link_url})!
"""

# Insert 20 sample posts into the database
for i in range(20):
    title = sample_titles[i % len(sample_titles)]
    author = sample_authors[i % len(sample_authors)]
    tags = ",".join(sample_tags[i % len(sample_tags):i % len(sample_tags) + 3])  # Randomly assign tags
    markdown_content = generate_markdown_content(title)
    
    # Convert the markdown content to HTML
    html_content = markdown(markdown_content)
    
    # Prepare SQL to insert the data
    cursor.execute('''INSERT INTO posts (post_title, post_content, post_author, tags)
                      VALUES (?, ?, ?, ?)''', (title, html_content, author, tags))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Sample posts inserted successfully!")
