#!/usr/bin/env python3
"""
Hashnode to GitHub Sync Script
Fetches articles from Hashnode and saves them as markdown files
"""

import os
import requests
import json
from datetime import datetime
from pathlib import Path
import re

# Configuration
HASHNODE_TOKEN = os.environ.get('HASHNODE_TOKEN')
BLOG_HOST = 'fabiolauria.hashnode.dev'

# GraphQL query to fetch articles
QUERY = """
query Publication($host: String!) {
  publication(host: $host) {
    posts(first: 50) {
      edges {
        node {
          id
          title
          slug
          brief
          content {
            markdown
          }
          coverImage {
            url
          }
          tags {
            name
          }
          publishedAt
          updatedAt
          url
        }
      }
    }
  }
}
"""

def slugify(text):
    """Convert title to filename-safe slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def fetch_articles():
    """Fetch articles from Hashnode API"""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': HASHNODE_TOKEN
    }
    
    response = requests.post(
        'https://gql.hashnode.com/',
        json={'query': QUERY, 'variables': {'host': BLOG_HOST}},
        headers=headers
    )
    
    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code} - {response.text}")
    
    data = response.json()
    
    if 'errors' in data:
        raise Exception(f"GraphQL errors: {data['errors']}")
    
    return data['data']['publication']['posts']['edges']

def save_article(article_node):
    """Save article as markdown file"""
    article = article_node['node']
    
    # Parse published date
    published_date = datetime.fromisoformat(article['publishedAt'].replace('Z', '+00:00'))
    year = published_date.strftime('%Y')
    month = published_date.strftime('%m')
    
    # Create directory structure: articles/YYYY/MM/
    article_dir = Path(f'articles/{year}/{month}')
    article_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    slug = article['slug']
    filename = article_dir / f"{slug}.md"
    
    # Prepare frontmatter
    tags = [tag['name'] for tag in article['tags']] if article['tags'] else []
    cover_image = article['coverImage']['url'] if article['coverImage'] else ''
    
    frontmatter = f"""---
title: "{article['title']}"
slug: "{slug}"
publishedAt: {article['publishedAt']}
updatedAt: {article['updatedAt']}
canonical: {article['url']}
tags: {', '.join(tags)}
coverImage: {cover_image}
brief: "{article['brief']}"
---

"""
    
    # Combine frontmatter and content
    content = frontmatter + article['content']['markdown']
    
    # Write to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Saved: {filename}")
    return filename

def main():
    """Main sync function"""
    if not HASHNODE_TOKEN:
        raise Exception("HASHNODE_TOKEN environment variable not set")
    
    print(f"🔄 Syncing articles from {BLOG_HOST}...")
    
    try:
        articles = fetch_articles()
        print(f"📚 Found {len(articles)} articles")
        
        saved_count = 0
        for article_edge in articles:
            try:
                save_article(article_edge)
                saved_count += 1
            except Exception as e:
                print(f"⚠️ Error saving article: {e}")
        
        print(f"\n✅ Sync complete! Saved {saved_count}/{len(articles)} articles")
        
    except Exception as e:
        print(f"❌ Sync failed: {e}")
        exit(1)

if __name__ == '__main__':
    main()
